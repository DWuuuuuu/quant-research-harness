"""Study 1: does cross-sectional momentum survive costs?

Run: python examples/01_single_factor_momentum.py

The question is not whether momentum ranks stocks. It is whether the ranking
survives the turnover it implies. This is why the frictionless comparison is
part of the study rather than an afterthought: the gap between the two lines
is the cost of the strategy's own impatience.
"""

from __future__ import annotations

from functools import partial

from _common import load_panel, report

from qrh.backtest.costs import CostModel
from qrh.backtest.engine import BacktestConfig, run_backtest
from qrh.indicators import momentum
from qrh.metrics import summary


def main() -> None:
    panel = load_panel()
    signal = partial(momentum, lookback=120, skip=5)
    results = {}

    for label, costs in (
        ("frictionless", CostModel.frictionless()),
        ("a-share costs", CostModel.a_share()),
    ):
        for rule in ("ME", "QE"):
            config = BacktestConfig(
                top_n=5, rebalance=rule, warmup_periods=140, costs=costs
            )
            result = run_backtest(panel, signal, config)
            name = f"{label}, {rule}"
            results[name] = summary(result.nav)
            results[name]["_costs"] = result.total_costs

    print("Study 1: cross-sectional momentum, top 5 of 24\n")
    print(report(results).to_string())
    print("\nCost drag (currency units):")
    for name, row in results.items():
        print(f"  {name:<24} {row['_costs']:>12,.0f}")
    print(
        "\nReading: compare each costed row against its frictionless twin at the\n"
        "same rebalance frequency. The monthly gap is the turnover tax."
    )


if __name__ == "__main__":
    main()
