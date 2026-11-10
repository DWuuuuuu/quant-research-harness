"""Performance and risk metrics computed from a NAV series.

Conventions used throughout:

* A *NAV series* is a pandas Series indexed by date, strictly positive, where
  the first value is the starting capital. Returns are derived from it rather
  than passed alongside it, so the two can never disagree.
* Drawdowns are reported as negative numbers (-0.25 is a 25% drawdown).
* Durations are reported in *periods*, not days, because the harness supports
  weekly and monthly rebalancing as well as daily.
* A metric that is undefined for the input returns ``float("nan")`` rather than
  raising, so that a summary table over many strategies never dies on one bad
  series. The one exception is a structurally invalid NAV (non-positive or
  non-monotonic index), which raises.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

TRADING_DAYS_PER_YEAR = 252


def _validate_nav(nav: pd.Series) -> pd.Series:
    """Return a cleaned NAV series, raising if it is structurally invalid."""
    if not isinstance(nav, pd.Series):
        raise TypeError(f"nav must be a pandas Series, got {type(nav).__name__}")
    nav = nav.dropna()
    if nav.empty:
        return nav
    if (nav <= 0).any():
        raise ValueError("NAV must be strictly positive; got a non-positive value")
    if not nav.index.is_monotonic_increasing:
        raise ValueError("NAV index must be sorted ascending")
    return nav


def to_returns(nav: pd.Series) -> pd.Series:
    """Simple period-over-period returns implied by a NAV series."""
    nav = _validate_nav(nav)
    return nav.pct_change().dropna()


def total_return(nav: pd.Series) -> float:
    """Cumulative return over the whole series."""
    nav = _validate_nav(nav)
    if len(nav) < 2:
        return float("nan")
    return float(nav.iloc[-1] / nav.iloc[0] - 1.0)


def _years_elapsed(nav: pd.Series, periods_per_year: int) -> float:
    """Elapsed time in years, from the index where possible.

    A DatetimeIndex gives the true elapsed calendar time, which matters when a
    strategy trades monthly but the index is irregular. Otherwise we fall back
    to counting periods.
    """
    if isinstance(nav.index, pd.DatetimeIndex) and len(nav) >= 2:
        days = int((nav.index[-1] - nav.index[0]).days)
        if days > 0:
            return days / 365.25
    return (len(nav) - 1) / periods_per_year


def cagr(nav: pd.Series, periods_per_year: int = TRADING_DAYS_PER_YEAR) -> float:
    """Compound annual growth rate."""
    nav = _validate_nav(nav)
    if len(nav) < 2:
        return float("nan")
    years = _years_elapsed(nav, periods_per_year)
    if years <= 0:
        return float("nan")
    return float((nav.iloc[-1] / nav.iloc[0]) ** (1.0 / years) - 1.0)


def annualised_volatility(
    nav: pd.Series, periods_per_year: int = TRADING_DAYS_PER_YEAR
) -> float:
    """Annualised standard deviation of period returns (sample, ddof=1)."""
    returns = to_returns(nav)
    if len(returns) < 2:
        return float("nan")
    return float(returns.std(ddof=1) * np.sqrt(periods_per_year))


def sharpe_ratio(
    nav: pd.Series,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
    risk_free_rate: float = 0.0,
) -> float:
    """Annualised Sharpe ratio.

    ``risk_free_rate`` is an *annual* rate; it is converted to a per-period
    rate geometrically so that the result is consistent with ``cagr``.
    """
    returns = to_returns(nav)
    if len(returns) < 2:
        return float("nan")
    rf_per_period = (1.0 + risk_free_rate) ** (1.0 / periods_per_year) - 1.0
    excess = returns - rf_per_period
    sd = excess.std(ddof=1)
    if sd == 0 or not np.isfinite(sd):
        return float("nan")
    return float(excess.mean() / sd * np.sqrt(periods_per_year))


def drawdown_series(nav: pd.Series) -> pd.Series:
    """Drawdown at each point, as a non-positive fraction of the running peak."""
    nav = _validate_nav(nav)
    if nav.empty:
        return nav
    return nav / nav.cummax() - 1.0


def max_drawdown(nav: pd.Series) -> float:
    """Worst peak-to-trough decline, as a negative fraction."""
    dd = drawdown_series(nav)
    if dd.empty:
        return float("nan")
    return float(dd.min())


def max_drawdown_duration(nav: pd.Series) -> float:
    """Longest run of periods spent below a previous peak.

    This is the metric that tends to decide whether a strategy is actually
    holdable: a 20% drawdown recovered in a month is a different experience
    from the same drawdown recovered in three years. An unrecovered drawdown
    at the end of the sample counts up to the final observation.
    """
    nav = _validate_nav(nav)
    if len(nav) < 2:
        return float("nan")
    underwater = (nav < nav.cummax()).to_numpy()
    longest = current = 0
    for flag in underwater:
        current = current + 1 if flag else 0
        longest = max(longest, current)
    return float(longest)


def recovery_duration(nav: pd.Series) -> float:
    """Periods from the maximum-drawdown trough back to the prior peak.

    Returns ``nan`` if the series never regains that peak, which is itself a
    result worth reporting rather than hiding.
    """
    nav = _validate_nav(nav)
    if len(nav) < 2:
        return float("nan")
    dd = drawdown_series(nav)
    trough_pos = int(np.argmin(dd.to_numpy()))
    if dd.iloc[trough_pos] == 0:
        return 0.0
    peak_before = float(nav.iloc[: trough_pos + 1].max())
    after = nav.iloc[trough_pos + 1 :]
    recovered = after[after >= peak_before]
    if recovered.empty:
        return float("nan")
    recovery_pos = nav.index.get_loc(recovered.index[0])
    return float(recovery_pos - trough_pos)


def mar_ratio(nav: pd.Series, periods_per_year: int = TRADING_DAYS_PER_YEAR) -> float:
    """CAGR divided by the absolute maximum drawdown.

    Undefined when the strategy never drew down, in which case we return
    ``inf`` rather than pretending the risk-adjusted return is finite.
    """
    growth = cagr(nav, periods_per_year)
    mdd = max_drawdown(nav)
    if not np.isfinite(growth) or not np.isfinite(mdd):
        return float("nan")
    if mdd == 0:
        return float("inf")
    return float(growth / abs(mdd))


def summary(
    nav: pd.Series,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
    risk_free_rate: float = 0.0,
) -> dict[str, float]:
    """The full metric suite, applied identically to every strategy.

    Returning a plain dict keeps this usable as a row in a comparison table::

        pd.DataFrame([summary(a), summary(b)], index=["a", "b"])
    """
    return {
        "total_return": total_return(nav),
        "cagr": cagr(nav, periods_per_year),
        "annualised_vol": annualised_volatility(nav, periods_per_year),
        "sharpe": sharpe_ratio(nav, periods_per_year, risk_free_rate),
        "max_drawdown": max_drawdown(nav),
        "mar": mar_ratio(nav, periods_per_year),
        "max_dd_duration_periods": max_drawdown_duration(nav),
        "recovery_periods": recovery_duration(nav),
        "n_periods": float(len(_validate_nav(nav))),
    }
