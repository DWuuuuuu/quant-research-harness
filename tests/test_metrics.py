"""Metric tests against hand-computable cases.

Every metric is checked against a series whose answer can be derived on paper.
Testing metrics against each other, or against a previous run, would only prove
the code is self-consistent.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from qrh.metrics import performance as perf


def nav_from(values: list[float], start: str = "2020-01-01") -> pd.Series:
    return pd.Series(values, index=pd.bdate_range(start, periods=len(values)))


class TestTotalReturnAndCagr:
    def test_total_return_is_end_over_start(self) -> None:
        assert perf.total_return(nav_from([100.0, 150.0])) == pytest.approx(0.5)

    def test_total_return_undefined_for_single_point(self) -> None:
        assert np.isnan(perf.total_return(nav_from([100.0])))

    def test_cagr_matches_doubling_over_roughly_one_year(self) -> None:
        nav = pd.Series(
            [100.0, 200.0],
            index=pd.DatetimeIndex(["2020-01-01", "2021-01-01"]),
        )
        # 2020 is a leap year, so the span is 366 days against a 365.25-day
        # year: slightly more than one year, hence slightly under 100%.
        # 2 ** (365.25 / 366) - 1 = 0.99716
        assert perf.cagr(nav) == pytest.approx(0.99716, abs=1e-4)

    def test_cagr_uses_period_count_without_a_datetime_index(self) -> None:
        nav = pd.Series([100.0, 200.0], index=[0, 1])
        # One period at 252 per year annualises to a very large number.
        assert perf.cagr(nav, periods_per_year=1) == pytest.approx(1.0)


class TestVolatilityAndSharpe:
    def test_zero_volatility_gives_nan_sharpe(self) -> None:
        # Constant NAV: no variation, so the ratio is undefined rather than 0.
        assert np.isnan(perf.sharpe_ratio(nav_from([100.0] * 10)))

    def test_sharpe_is_annualised_by_root_periods(self) -> None:
        rng = np.random.default_rng(0)
        returns = rng.normal(0.001, 0.01, 500)
        nav = nav_from(list(100.0 * np.cumprod(1.0 + returns)))
        daily = perf.sharpe_ratio(nav, periods_per_year=1)
        annual = perf.sharpe_ratio(nav, periods_per_year=252)
        assert annual == pytest.approx(daily * np.sqrt(252), rel=1e-9)

    def test_volatility_needs_two_returns(self) -> None:
        assert np.isnan(perf.annualised_volatility(nav_from([100.0, 101.0])))


class TestDrawdown:
    # Peak 120 at index 2, trough 60 at index 4, recovers to 120 at index 7.
    nav = nav_from([100.0, 110.0, 120.0, 90.0, 60.0, 80.0, 110.0, 120.0, 130.0])

    def test_max_drawdown_is_trough_over_prior_peak(self) -> None:
        assert perf.max_drawdown(self.nav) == pytest.approx(60.0 / 120.0 - 1.0)

    def test_drawdown_is_zero_at_new_highs(self) -> None:
        dd = perf.drawdown_series(self.nav)
        assert dd.iloc[0] == 0.0
        assert dd.iloc[2] == 0.0
        assert dd.iloc[-1] == 0.0

    def test_duration_counts_periods_below_the_peak(self) -> None:
        # Indices 3,4,5,6 are below 120; index 7 regains it.
        assert perf.max_drawdown_duration(self.nav) == 4.0

    def test_recovery_runs_from_trough_to_the_old_peak(self) -> None:
        # Trough at index 4, 120 regained at index 7.
        assert perf.recovery_duration(self.nav) == 3.0

    def test_recovery_is_nan_when_never_regained(self) -> None:
        never = nav_from([100.0, 50.0, 60.0, 70.0])
        assert np.isnan(perf.recovery_duration(never))

    def test_monotonic_series_has_no_drawdown(self) -> None:
        rising = nav_from([100.0, 101.0, 102.0, 103.0])
        assert perf.max_drawdown(rising) == 0.0
        assert perf.max_drawdown_duration(rising) == 0.0
        assert perf.recovery_duration(rising) == 0.0


class TestMar:
    def test_mar_is_cagr_over_absolute_drawdown(self) -> None:
        nav = nav_from([100.0, 120.0, 90.0, 150.0])
        expected = perf.cagr(nav) / abs(perf.max_drawdown(nav))
        assert perf.mar_ratio(nav) == pytest.approx(expected)

    def test_mar_is_infinite_without_a_drawdown(self) -> None:
        assert perf.mar_ratio(nav_from([100.0, 110.0, 120.0])) == float("inf")


class TestValidation:
    def test_non_positive_nav_raises(self) -> None:
        with pytest.raises(ValueError, match="strictly positive"):
            perf.max_drawdown(nav_from([100.0, 0.0, 50.0]))

    def test_unsorted_index_raises(self) -> None:
        nav = pd.Series([100.0, 110.0], index=pd.DatetimeIndex(["2020-02-01", "2020-01-01"]))
        with pytest.raises(ValueError, match="sorted ascending"):
            perf.max_drawdown(nav)

    def test_non_series_raises(self) -> None:
        with pytest.raises(TypeError):
            perf.max_drawdown([100.0, 110.0])  # type: ignore[arg-type]

    def test_summary_survives_a_degenerate_series(self) -> None:
        # One point is not enough for most metrics, but a summary table over
        # many strategies must not die because one of them is a stub.
        out = perf.summary(nav_from([100.0]))
        assert out["n_periods"] == 1.0
        assert np.isnan(out["sharpe"])


def test_summary_reports_the_full_suite() -> None:
    expected = {
        "total_return",
        "cagr",
        "annualised_vol",
        "sharpe",
        "max_drawdown",
        "mar",
        "max_dd_duration_periods",
        "recovery_periods",
        "n_periods",
    }
    assert set(perf.summary(nav_from([100.0, 110.0, 105.0, 130.0]))) == expected
