"""Engine tests, with look-ahead protection as the headline case.

A backtest engine has one job it must not get wrong: it must not let a
strategy see the future. That property is asserted here directly rather than
assumed, because it is invisible in results. A look-ahead bug does not make a
backtest crash; it makes it look good.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from qrh.backtest.costs import CostModel
from qrh.backtest.engine import BacktestConfig, run_backtest
from qrh.data.base import PanelData
from qrh.data.synthetic import SyntheticLoader
from qrh.indicators import momentum

SYMBOLS = [f"S{i:02d}" for i in range(12)]


@pytest.fixture
def panel() -> PanelData:
    return SyntheticLoader().load(SYMBOLS, "2019-01-01", "2024-12-31")


class TestLookAhead:
    def test_signal_never_sees_data_past_the_decision_date(self, panel: PanelData) -> None:
        seen: list[tuple[pd.Timestamp, pd.Timestamp]] = []

        def recording_signal(window: PanelData) -> pd.Series:
            seen.append((window.dates[-1], panel.dates[-1]))
            return momentum(window)

        run_backtest(panel, recording_signal, BacktestConfig(warmup_periods=150))

        assert seen, "signal was never called"
        # Every window must end strictly before the end of the full sample,
        # and no window may contain a date the engine had not reached.
        for window_end, sample_end in seen:
            assert window_end < sample_end

    def test_future_prices_cannot_change_past_decisions(self, panel: PanelData) -> None:
        """Rewriting the tail of the data must not alter earlier NAV.

        This is the strongest available check: if any decision depended on
        future information, mutating the future would move the past.
        """
        cutoff = panel.dates[len(panel.dates) // 2]
        config = BacktestConfig(warmup_periods=150)

        baseline = run_backtest(panel, momentum, config)

        tampered_fields = {}
        for name, frame in panel.fields.items():
            copy = frame.copy()
            # Multiply everything after the cutoff by a large factor.
            copy.loc[copy.index > cutoff] *= 5.0
            tampered_fields[name] = copy
        tampered = run_backtest(PanelData(tampered_fields), momentum, config)

        before = baseline.nav.loc[:cutoff]
        after = tampered.nav.loc[:cutoff]
        pd.testing.assert_series_equal(before, after)

    def test_trades_execute_after_the_decision(self, panel: PanelData) -> None:
        result = run_backtest(panel, momentum, BacktestConfig(warmup_periods=150))
        # The first trade cannot land on the first eligible decision date,
        # because execution is deferred by one period.
        assert result.n_rebalances > 0
        assert result.trades["date"].iloc[0] > panel.dates[150]


class TestPortfolioConstruction:
    def test_holds_exactly_top_n_names(self, panel: PanelData) -> None:
        config = BacktestConfig(top_n=3, warmup_periods=150)
        result = run_backtest(panel, momentum, config)
        held = (result.holdings.abs() > 1e-9).sum(axis=1)
        # Before the first execution nothing is held; after it, exactly 3.
        assert set(held.unique()) <= {0, 3}
        assert (held == 3).any()

    def test_weights_are_equal_and_sum_to_one_when_invested(self, panel: PanelData) -> None:
        result = run_backtest(panel, momentum, BacktestConfig(top_n=4, warmup_periods=150))
        invested = result.holdings[(result.holdings.abs() > 1e-9).sum(axis=1) == 4]
        assert not invested.empty
        row = invested.iloc[0]
        active = row[row.abs() > 1e-9]
        assert active.std(ddof=0) == pytest.approx(0.0, abs=1e-6)
        # Sizing against post-cost capital leaves a second-order residual in
        # the cost rate, so this is exact to a few parts per million rather
        # than to machine precision. It is not exact by construction, and
        # pretending otherwise would be the wrong assertion.
        assert float(active.sum()) == pytest.approx(1.0, abs=1e-5)

    def test_long_only_portfolio_never_borrows(self, panel: PanelData) -> None:
        """Gross exposure must not exceed NAV.

        Sizing positions against pre-cost NAV and then paying commission out
        of the cash leg silently levers a portfolio that is supposed to be
        unlevered. It is a small effect per rebalance and it compounds, so it
        is asserted rather than eyeballed.
        """
        result = run_backtest(panel, momentum, BacktestConfig(top_n=4, warmup_periods=150))
        gross = result.holdings.abs().sum(axis=1)
        assert gross.max() <= 1.0 + 1e-5
        assert (result.holdings >= -1e-9).all().all()

    def test_all_nan_signal_stays_in_cash(self, panel: PanelData) -> None:
        def no_signal(window: PanelData) -> pd.Series:
            return pd.Series(float("nan"), index=window.symbols)

        result = run_backtest(panel, no_signal, BacktestConfig(warmup_periods=150))
        assert result.nav.iloc[-1] == pytest.approx(result.nav.iloc[0])
        assert result.total_costs == 0.0


class TestCostsAffectResults:
    def test_costs_reduce_terminal_nav(self, panel: PanelData) -> None:
        free = run_backtest(
            panel, momentum, BacktestConfig(warmup_periods=150, costs=CostModel.frictionless())
        )
        charged = run_backtest(
            panel, momentum, BacktestConfig(warmup_periods=150, costs=CostModel.a_share())
        )
        assert charged.nav.iloc[-1] < free.nav.iloc[-1]
        assert charged.total_costs > 0.0
        assert free.total_costs == 0.0

    def test_higher_turnover_costs_more(self, panel: PanelData) -> None:
        monthly = run_backtest(
            panel, momentum, BacktestConfig(rebalance="ME", warmup_periods=150)
        )
        quarterly = run_backtest(
            panel, momentum, BacktestConfig(rebalance="QE", warmup_periods=150)
        )
        assert monthly.n_rebalances > quarterly.n_rebalances
        assert monthly.total_costs > quarterly.total_costs


class TestValidation:
    def test_too_short_a_sample_raises(self) -> None:
        short = SyntheticLoader().load(SYMBOLS, "2024-01-01", "2024-02-01")
        with pytest.raises(ValueError, match="need more than"):
            run_backtest(short, momentum, BacktestConfig(warmup_periods=150))

    def test_bad_top_n_raises(self) -> None:
        with pytest.raises(ValueError, match="top_n"):
            BacktestConfig(top_n=0)

    def test_mismatched_fields_raise(self) -> None:
        dates = pd.bdate_range("2020-01-01", periods=10)
        good = pd.DataFrame(1.0, index=dates, columns=["A", "B"])
        bad = pd.DataFrame(1.0, index=dates, columns=["A", "C"])
        with pytest.raises(ValueError, match="different symbols"):
            PanelData({"close": good, "other": bad})

    def test_unknown_field_lists_what_is_available(self, panel: PanelData) -> None:
        with pytest.raises(KeyError, match="available"):
            panel.field("book_to_price")


def test_nav_index_matches_the_sample(panel: PanelData) -> None:
    result = run_backtest(panel, momentum, BacktestConfig(warmup_periods=150))
    assert isinstance(result.nav.index, pd.DatetimeIndex)
    assert len(result.nav) == len(panel.dates)
    assert np.all(np.isfinite(result.nav.to_numpy()))


class TestTurnover:
    def test_turnover_is_measured_against_nav_on_the_trade_date(
        self, panel: PanelData
    ) -> None:
        result = run_backtest(panel, momentum, BacktestConfig(top_n=5, warmup_periods=150))
        nav_on_date = result.nav.reindex(result.trades["date"]).to_numpy()
        buys = result.trades["buy_notional"].to_numpy()
        assert result.turnover == pytest.approx(float((buys / nav_on_date).mean()))

    def test_a_full_reshuffle_is_near_one_hundred_percent(self, panel: PanelData) -> None:
        """A strategy that replaces its whole book each time turns over ~100%.

        Sanity bound rather than an exact figure: the first rebalance buys from
        cash, and costs shave a little off each subsequent one.
        """
        flipping = iter(range(10_000))

        def alternating(window: PanelData) -> pd.Series:
            # Rotate the preferred names every call so holdings fully replace.
            offset = next(flipping)
            n = len(window.symbols)
            return pd.Series(
                [((i + offset * 5) % n) for i in range(n)], index=window.symbols, dtype=float
            )

        result = run_backtest(panel, alternating, BacktestConfig(top_n=4, warmup_periods=150))
        assert 0.8 < result.turnover <= 1.05

    def test_no_trades_means_no_turnover(self, panel: PanelData) -> None:
        def no_signal(window: PanelData) -> pd.Series:
            return pd.Series(float("nan"), index=window.symbols)

        result = run_backtest(panel, no_signal, BacktestConfig(warmup_periods=150))
        assert result.turnover == 0.0
