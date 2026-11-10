"""Study 3: short-horizon mean reversion. A negative result, kept on purpose.

Run: python examples/03_rejected_mean_reversion.py

This strategy does not work, and it is in the repository for that reason.
Most ideas fail; a research process that only records the survivors produces a
track record that cannot be trusted, because the reader has no way to know how
many attempts preceded it.

The specific failure is instructive. Reversion ranks well enough frictionless
to look tempting, and then loses the entire edge to the turnover required to
harvest it. That pattern is the single most common way a backtest misleads.
"""

from __future__ import annotations

import pandas as pd
from _common import load_panel, report

from qrh.backtest.costs import CostModel
from qrh.backtest.engine import BacktestConfig, run_backtest
from qrh.data.base import PanelData
from qrh.metrics import summary


def short_term_reversal(panel: PanelData, lookback: int = 5) -> pd.Series:
    """Buy the recent losers: the negative of short-horizon return."""
    close = panel.field("close")
    if len(close) < lookback + 1:
        return pd.Series(float("nan"), index=close.columns)
    recent = close.iloc[-1] / close.iloc[-(lookback + 1)] - 1.0
    return -recent


def main() -> None:
    panel = load_panel()
    results = {}

    for label, rule, costs in (
        ("weekly, frictionless", "W-FRI", CostModel.frictionless()),
        ("weekly, a-share costs", "W-FRI", CostModel.a_share()),
        ("monthly, frictionless", "ME", CostModel.frictionless()),
        ("monthly, a-share costs", "ME", CostModel.a_share()),
    ):
        config = BacktestConfig(
            top_n=5, rebalance=rule, warmup_periods=60, costs=costs
        )
        result = run_backtest(panel, short_term_reversal, config)
        results[label] = summary(result.nav)
        results[label]["_costs"] = result.total_costs
        results[label]["_rebalances"] = float(result.n_rebalances)

    print("Study 3: short-horizon reversal, top 5 of 24 (REJECTED)\n")
    print(report(results).to_string())
    print("\nRebalances and cost drag:")
    for name, row in results.items():
        print(f"  {name:<24} {int(row['_rebalances']):>5} rebalances  {row['_costs']:>12,.0f}")

    print(
        "\nVerdict: rejected. The frictionless-to-costed gap is the whole story,\n"
        "and it widens with rebalance frequency. Nothing here is worth capital."
    )


if __name__ == "__main__":
    main()
