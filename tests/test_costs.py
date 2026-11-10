"""Cost-model tests.

The asymmetry between buys and sells, and the per-trade floor, are the parts
that change strategy ranking, so they are tested directly.
"""

from __future__ import annotations

import pytest

from qrh.backtest.costs import CostModel, dividend_tax_rate


class TestTradeCost:
    def test_no_trading_costs_nothing(self) -> None:
        assert CostModel.a_share().trade_cost(0.0, 0.0) == 0.0

    def test_stamp_duty_falls_on_sales_only(self) -> None:
        model = CostModel(commission_rate=0.0, stamp_duty_rate=0.001, slippage_rate=0.0)
        assert model.trade_cost(buy_notional=10_000.0, sell_notional=0.0) == 0.0
        sell_only = model.trade_cost(buy_notional=0.0, sell_notional=10_000.0)
        assert sell_only == pytest.approx(10.0)

    def test_commission_and_slippage_apply_to_both_sides(self) -> None:
        model = CostModel(
            commission_rate=0.0001, stamp_duty_rate=0.0, slippage_rate=0.0002
        )
        # 1,000 + 1,000 traded at 3bp total.
        assert model.trade_cost(1_000.0, 1_000.0) == pytest.approx(0.6)

    def test_minimum_commission_dominates_small_trades(self) -> None:
        model = CostModel(
            commission_rate=0.0001,
            stamp_duty_rate=0.0,
            slippage_rate=0.0,
            min_commission=5.0,
        )
        # 100 notional would imply 1 cent of commission; the floor applies.
        assert model.trade_cost(100.0, 0.0) == pytest.approx(5.0)

    def test_frictionless_is_actually_free(self) -> None:
        assert CostModel.frictionless().trade_cost(1e9, 1e9) == 0.0

    def test_negative_notional_raises(self) -> None:
        with pytest.raises(ValueError):
            CostModel.a_share().trade_cost(-1.0, 0.0)

    def test_us_equity_has_no_stamp_duty(self) -> None:
        assert CostModel.us_equity().stamp_duty_rate == 0.0


class TestDividendTax:
    @pytest.mark.parametrize(
        "days,expected",
        [(0, 0.20), (30, 0.20), (31, 0.10), (365, 0.10), (366, 0.0), (10_000, 0.0)],
    )
    def test_rate_steps_down_at_the_boundaries(self, days: int, expected: float) -> None:
        assert dividend_tax_rate(days) == expected

    def test_negative_holding_period_raises(self) -> None:
        with pytest.raises(ValueError):
            dividend_tax_rate(-1)
