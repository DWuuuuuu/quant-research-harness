"""A cross-sectional, long-only, equal-weight backtest engine.

Scope:

* Long only. Borrow cost, recall risk and squeeze exposure make short legs a
  poor fit for a small account, and A-share retail shorting barely exists.
* Equal weight within the selected set. Optimised weights need a covariance
  estimate, which on a short sample is mostly estimation error.
* Signals use data up to and including the rebalance date; trades execute at
  the next period's close. The engine enforces that gap rather than leaving it
  to the strategy author.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from qrh.backtest.costs import CostModel
from qrh.data.base import PanelData

SignalFn = Callable[[PanelData], pd.Series]


@dataclass(frozen=True)
class BacktestConfig:
    """How a single study is run.

    Parameters
    ----------
    top_n:
        Number of symbols held, equal weighted.
    rebalance:
        Pandas offset alias for rebalance dates (``"ME"`` month-end,
        ``"W-FRI"`` weekly, ``"QE"`` quarterly).
    warmup_periods:
        Periods skipped before the first trade, so that indicators needing
        history are not evaluated on a stub.
    initial_capital:
        Starting NAV.
    costs:
        Cost model; defaults to A-share conventions.
    """

    top_n: int = 5
    rebalance: str = "ME"
    warmup_periods: int = 130
    initial_capital: float = 1_000_000.0
    costs: CostModel = field(default_factory=CostModel.a_share)

    def __post_init__(self) -> None:
        if self.top_n < 1:
            raise ValueError("top_n must be at least 1")
        if self.warmup_periods < 0:
            raise ValueError("warmup_periods must be non-negative")
        if self.initial_capital <= 0:
            raise ValueError("initial_capital must be positive")


@dataclass
class BacktestResult:
    """Everything a study produces.

    ``nav`` is the series every metric is computed from. ``holdings`` and
    ``trades`` are kept so that a surprising result can be traced back to the
    positions that caused it, which is usually how a bug is found.
    """

    nav: pd.Series
    holdings: pd.DataFrame
    trades: pd.DataFrame
    total_costs: float
    n_rebalances: int

    @property
    def turnover(self) -> float:
        """Mean one-way turnover per rebalance, as a fraction of NAV that day.

        Each rebalance is measured against the NAV it actually traded against,
        then averaged. Dividing total buys by a time-averaged NAV instead will
        understate turnover for a strategy whose NAV grew, and overstate it for
        one that shrank.
        """
        if self.trades.empty:
            return 0.0
        nav_on_trade_date = self.nav.reindex(self.trades["date"]).to_numpy()
        buys = self.trades["buy_notional"].to_numpy()
        usable = np.isfinite(nav_on_trade_date) & (nav_on_trade_date > 0)
        if not usable.any():
            return 0.0
        return float(np.mean(buys[usable] / nav_on_trade_date[usable]))


def _rebalance_dates(
    dates: pd.DatetimeIndex, rule: str, warmup: int
) -> pd.DatetimeIndex:
    """Dates on which the portfolio is re-selected, after warmup."""
    if warmup >= len(dates):
        return pd.DatetimeIndex([])
    eligible = dates[warmup:]
    if eligible.empty:
        return pd.DatetimeIndex([])
    # Take the last available observation in each period, which is the real
    # decision point; resampling the index itself would invent dates on which
    # the market was closed.
    grouped = pd.Series(eligible, index=eligible).resample(rule).last().dropna()
    return pd.DatetimeIndex(grouped.to_numpy())


def _price_trade(
    investable: float,
    weights: pd.Series,
    prices: pd.Series,
    shares: pd.Series,
    costs: CostModel,
) -> tuple[pd.Series, float, float, float]:
    """Size a target portfolio and price the trade that reaches it.

    Returns the target share counts alongside gross buy notional, gross sell
    notional and total cost. Kept separate from the main loop so that it can
    be called twice per rebalance (once to discover the cost, once to re-size
    against the capital that survives it) without capturing loop state.
    """
    target_value = investable * weights
    with np.errstate(divide="ignore", invalid="ignore"):
        target_shares = (
            (target_value / prices).replace([np.inf, -np.inf], np.nan).fillna(0.0)
        )
    delta = target_shares - shares
    buys = float((delta.clip(lower=0) * prices).sum())
    sells = float((-delta.clip(upper=0) * prices).sum())
    return target_shares, buys, sells, costs.trade_cost(buys, sells)


def run_backtest(
    panel: PanelData,
    signal: SignalFn,
    config: BacktestConfig | None = None,
) -> BacktestResult:
    """Run one study and return its NAV plus the audit trail.

    The loop holds shares, not weights, so that drift between rebalances is
    real rather than assumed away, and so that costs apply to the notional
    actually traded.
    """
    config = config or BacktestConfig()
    close = panel.field("close")
    dates = panel.dates
    if len(dates) < config.warmup_periods + 2:
        raise ValueError(
            f"need more than {config.warmup_periods + 1} periods, got {len(dates)}"
        )

    rebalance_on = set(_rebalance_dates(dates, config.rebalance, config.warmup_periods))
    if not rebalance_on:
        raise ValueError("no rebalance dates; check the rebalance rule and warmup")

    cash = config.initial_capital
    shares = pd.Series(0.0, index=panel.symbols, dtype=float)
    nav_records: list[tuple[pd.Timestamp, float]] = []
    holding_records: dict[pd.Timestamp, pd.Series] = {}
    trade_records: list[dict[str, float | pd.Timestamp]] = []
    total_costs = 0.0
    n_rebalances = 0
    pending: pd.Series | None = None

    for i, date in enumerate(dates):
        prices = close.loc[date]

        # Execute whatever the previous period decided, at today's close.
        if pending is not None:
            total_value = cash + float((shares * prices).sum())

            # Costs are funded out of the same capital, so allocating the full
            # NAV and then paying commission would overdraw the cash leg and
            # quietly lever a long-only portfolio. Price the trade once to
            # discover the cost, then re-size against the capital that
            # survives it. One pass suffices: the correction is second order
            # in the cost rate.
            _, _, _, provisional = _price_trade(
                total_value, pending, prices, shares, config.costs
            )
            target_shares, buy_notional, sell_notional, cost = _price_trade(
                max(total_value - provisional, 0.0), pending, prices, shares, config.costs
            )

            cash += sell_notional - buy_notional - cost
            shares = target_shares
            total_costs += cost
            n_rebalances += 1
            trade_records.append(
                {
                    "date": date,
                    "buy_notional": buy_notional,
                    "sell_notional": sell_notional,
                    "cost": cost,
                }
            )
            pending = None

        nav = cash + float((shares * prices).sum())
        if nav <= 0:
            raise RuntimeError(f"NAV went non-positive on {date.date()}")
        nav_records.append((date, nav))
        holding_records[date] = shares * prices / nav

        # Decide on rebalance dates using only data up to today, and act next.
        if date in rebalance_on and i < len(dates) - 1:
            scores = signal(panel.as_of(date)).reindex(panel.symbols)
            ranked = scores.dropna().sort_values(ascending=False)
            selected = list(ranked.index[: config.top_n])
            weights = pd.Series(0.0, index=panel.symbols, dtype=float)
            if selected:
                weights.loc[selected] = 1.0 / len(selected)
            pending = weights

    nav_series = pd.Series(dict(nav_records)).sort_index()
    nav_series.index = pd.DatetimeIndex(nav_series.index)
    return BacktestResult(
        nav=nav_series,
        holdings=pd.DataFrame(holding_records).T.sort_index(),
        trades=pd.DataFrame(trade_records),
        total_costs=total_costs,
        n_rebalances=n_rebalances,
    )
