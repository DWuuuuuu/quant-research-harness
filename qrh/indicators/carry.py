"""Yield-based indicators."""

from __future__ import annotations

import pandas as pd

from qrh.data.base import PanelData


def dividend_yield(panel: PanelData, smoothing: int = 20) -> pd.Series:
    """Dividend yield, averaged over the last ``smoothing`` periods.

    Smoothing matters because a point-in-time yield jumps on the ex-dividend
    date, which would otherwise show up as a spurious ranking change.
    """
    frame = panel.field("dividend_yield")
    if frame.empty:
        return pd.Series(float("nan"), index=frame.columns)
    window = frame.iloc[-min(smoothing, len(frame)) :]
    return window.mean()
