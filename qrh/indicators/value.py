"""Valuation indicators."""

from __future__ import annotations

import pandas as pd

from qrh.data.base import PanelData


def earnings_yield(panel: PanelData, smoothing: int = 20) -> pd.Series:
    """Earnings yield (the reciprocal of P/E), smoothed.

    Expressed as a yield rather than as P/E so that higher is always better,
    which keeps the sign convention uniform across indicators, and so that the
    metric stays finite as earnings approach zero.
    """
    frame = panel.field("earnings_yield")
    if frame.empty:
        return pd.Series(float("nan"), index=frame.columns)
    window = frame.iloc[-min(smoothing, len(frame)) :]
    return window.mean()
