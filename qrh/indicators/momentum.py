"""Price momentum."""

from __future__ import annotations

import numpy as np
import pandas as pd

from qrh.data.base import PanelData


def momentum(panel: PanelData, lookback: int = 120, skip: int = 5) -> pd.Series:
    """Total return over ``lookback`` periods, skipping the most recent ``skip``.

    The skip is not decoration. Very recent returns are contaminated by
    short-term reversal and by microstructure effects, and including them
    reliably weakens a medium-horizon momentum signal.
    """
    close = panel.field("close")
    needed = lookback + skip + 1
    if len(close) < needed:
        return pd.Series(float("nan"), index=close.columns)
    end = close.iloc[-(skip + 1)]
    start = close.iloc[-(skip + 1 + lookback)]
    return (end / start - 1.0).replace([np.inf, -np.inf], np.nan)


def risk_adjusted_momentum(
    panel: PanelData, lookback: int = 120, skip: int = 5
) -> pd.Series:
    """Momentum divided by realised volatility over the same window."""
    close = panel.field("close")
    needed = lookback + skip + 1
    if len(close) < needed:
        return pd.Series(float("nan"), index=close.columns)
    raw = momentum(panel, lookback=lookback, skip=skip)
    window = close.iloc[-(skip + 1 + lookback) : len(close) - skip]
    vol = window.pct_change().std(ddof=1)
    return (raw / vol.replace(0.0, np.nan)).replace([np.inf, -np.inf], np.nan)
