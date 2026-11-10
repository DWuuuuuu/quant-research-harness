"""Transaction and tax costs.

Costs scale with turnover while edge per trade does not, so a weekly strategy
needs roughly an order of magnitude more gross alpha than an annual one to
break even. At the horizons this harness targets they change strategy
rankings, not just levels.

The A-share defaults carry two asymmetries worth keeping: stamp duty applies
to sales only, and dividend tax depends on holding period. Verify current
rates before trading on them. They are here to make the mechanism explicit,
not as tax advice.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CostModel:
    """Proportional costs applied to traded notional.

    Parameters
    ----------
    commission_rate:
        Charged on both buys and sells.
    stamp_duty_rate:
        Charged on sales only (A-share convention).
    slippage_rate:
        A flat haircut standing in for market impact. Crude, and deliberately
        conservative: a more honest model would scale with participation rate,
        which this harness does not attempt because it holds no volume data.
    min_commission:
        Per-trade floor, which is what makes very small positions uneconomic.
    """

    commission_rate: float = 0.00025
    stamp_duty_rate: float = 0.0005
    slippage_rate: float = 0.0005
    min_commission: float = 0.0

    def trade_cost(self, buy_notional: float, sell_notional: float) -> float:
        """Total cost of a rebalance given gross buy and sell notional."""
        if buy_notional < 0 or sell_notional < 0:
            raise ValueError("notional must be non-negative")
        traded = buy_notional + sell_notional
        if traded == 0:
            return 0.0
        commission = max(traded * self.commission_rate, self.min_commission)
        return commission + sell_notional * self.stamp_duty_rate + traded * self.slippage_rate

    @classmethod
    def a_share(cls) -> CostModel:
        """Defaults in the right neighbourhood for mainland A-shares."""
        return cls(
            commission_rate=0.00025,
            stamp_duty_rate=0.0005,
            slippage_rate=0.0010,
            min_commission=5.0,
        )

    @classmethod
    def us_equity(cls) -> CostModel:
        """Defaults for a retail US equity account: no commission, no stamp duty."""
        return cls(
            commission_rate=0.0,
            stamp_duty_rate=0.0,
            slippage_rate=0.0005,
            min_commission=0.0,
        )

    @classmethod
    def frictionless(cls) -> CostModel:
        """Zero costs, for isolating the effect of the cost model itself.

        Useful as a diagnostic: if a strategy only works frictionless, the
        finding is about turnover, not about the signal.
        """
        return cls(0.0, 0.0, 0.0, 0.0)


def dividend_tax_rate(holding_period_days: int) -> float:
    """A-share dividend tax by holding period.

    Rates step down with holding period (20% at a month or less, 10% up to a
    year, nil beyond), which is a direct subsidy to patience and one reason
    this harness is built for monthly rather than daily rebalancing.
    """
    if holding_period_days < 0:
        raise ValueError("holding period cannot be negative")
    if holding_period_days <= 30:
        return 0.20
    if holding_period_days <= 365:
        return 0.10
    return 0.0
