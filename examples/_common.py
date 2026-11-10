"""Shared setup for the example studies.

Every example runs against the synthetic loader so that results are
reproducible without a data vendor account. Swap in a real adapter and the
rest of the code is unchanged.
"""

from __future__ import annotations

import pandas as pd

from qrh.data import SyntheticLoader
from qrh.data.base import PanelData

UNIVERSE = [f"S{i:02d}" for i in range(24)]
START, END = "2016-01-01", "2026-06-30"


def load_panel() -> PanelData:
    return SyntheticLoader().load(UNIVERSE, START, END)


def report(rows: dict[str, dict[str, float]]) -> pd.DataFrame:
    """Format a set of summaries as a comparison table."""
    frame = pd.DataFrame(rows).T
    display = frame[
        ["cagr", "annualised_vol", "sharpe", "max_drawdown", "mar", "recovery_periods"]
    ].copy()
    for col in ("cagr", "annualised_vol", "max_drawdown"):
        display[col] = (display[col] * 100).round(2)
    display["sharpe"] = display["sharpe"].round(2)
    display["mar"] = display["mar"].round(2)
    display.columns = [
        "CAGR %",
        "Vol %",
        "Sharpe",
        "MaxDD %",
        "MAR",
        "Recovery (periods)",
    ]
    return display
