"""Study 2: does blending yield with momentum help, and is it robust?

Run: python examples/02_blended_factors.py

A blend that beats its components on one parameter setting has told you
nothing. The sweep below is the actual result: if performance is a knife edge
in the weight, the apparent improvement is sample-fitting, and the right
conclusion is to discard it rather than to report the best cell.
"""

from __future__ import annotations

import pandas as pd
from _common import load_panel, report

from qrh.backtest.engine import BacktestConfig, run_backtest
from qrh.data.base import PanelData
from qrh.indicators import dividend_yield, momentum
from qrh.indicators.base import blend
from qrh.metrics import summary

CONFIG = BacktestConfig(top_n=5, rebalance="ME", warmup_periods=140)


def make_blend(momentum_weight: float):
    def signal(panel: PanelData) -> pd.Series:
        return blend(
            {"momentum": momentum_weight, "yield": 1.0 - momentum_weight},
            {"momentum": momentum(panel), "yield": dividend_yield(panel)},
        )

    return signal


def main() -> None:
    panel = load_panel()

    components = {
        "momentum only": summary(run_backtest(panel, momentum, CONFIG).nav),
        "yield only": summary(run_backtest(panel, dividend_yield, CONFIG).nav),
    }
    print("Study 2a: single factors\n")
    print(report(components).to_string())

    sweep = {}
    for weight in (0.0, 0.25, 0.4, 0.5, 0.6, 0.75, 1.0):
        label = f"momentum {weight:.0%} / yield {1 - weight:.0%}"
        sweep[label] = summary(run_backtest(panel, make_blend(weight), CONFIG).nav)

    print("\nStudy 2b: blend weight sweep\n")
    print(report(sweep).to_string())

    sharpes = pd.Series({k: v["sharpe"] for k, v in sweep.items()})
    print(
        f"\nSharpe across the sweep: min {sharpes.min():.2f}, max {sharpes.max():.2f}, "
        f"spread {sharpes.max() - sharpes.min():.2f}"
    )
    print(
        "Reading: a blend is only interesting if the sweep is flat near the\n"
        "optimum. A single standout cell surrounded by weak ones is an\n"
        "artefact of this sample, not a finding."
    )


if __name__ == "__main__":
    main()
