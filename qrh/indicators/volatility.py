"""Risk-based indicators."""

from __future__ import annotations

import numpy as np
import pandas as pd

from qrh.data.base import PanelData


def inverse_volatility(panel: PanelData, lookback: int = 60) -> pd.Series:
    """Reciprocal of trailing realised volatility, so low vol ranks high."""
    close = panel.field("close")
    if len(close) < lookback + 1:
        return pd.Series(float("nan"), index=close.columns)
    vol = close.iloc[-(lookback + 1) :].pct_change().std(ddof=1)
    return (1.0 / vol.replace(0.0, np.nan)).replace([np.inf, -np.inf], np.nan)
