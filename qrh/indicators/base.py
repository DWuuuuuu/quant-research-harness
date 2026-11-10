"""The indicator contract, plus the helpers most indicators need."""

from __future__ import annotations

from typing import Protocol

import pandas as pd

from qrh.data.base import PanelData


class Indicator(Protocol):
    """A cross-sectional score, higher meaning more attractive.

    An indicator receives only data that was available at decision time: the
    engine passes a :meth:`~qrh.data.base.PanelData.as_of` slice. Returning
    ``NaN`` for a symbol excludes it from selection on that date, which is the
    correct way to handle insufficient history.
    """

    def __call__(self, panel: PanelData) -> pd.Series:
        ...


def zscore(scores: pd.Series) -> pd.Series:
    """Cross-sectional z-score, NaNs preserved.

    Used to put indicators on a comparable scale before blending them. With
    fewer than two valid observations the result is undefined and all-NaN.
    """
    valid = scores.dropna()
    if len(valid) < 2:
        return pd.Series(float("nan"), index=scores.index)
    sd = valid.std(ddof=1)
    if sd == 0 or not pd.notna(sd):
        return pd.Series(float("nan"), index=scores.index)
    return (scores - valid.mean()) / sd


def blend(weights: dict[str, float], scores: dict[str, pd.Series]) -> pd.Series:
    """Weighted blend of z-scored indicators.

    Blending raw indicator values is a common and quiet error: dividend yield
    at 0.03 and a momentum value of 0.4 are not on the same scale, so the
    blend is dominated by whichever happens to have the larger variance. This
    z-scores each component first.
    """
    missing = set(weights) - set(scores)
    if missing:
        raise KeyError(f"no scores supplied for: {sorted(missing)}")
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("blend weights must sum to a positive number")
    combined: pd.Series | None = None
    for name, weight in weights.items():
        component = zscore(scores[name]) * (weight / total)
        combined = component if combined is None else combined.add(component)
    assert combined is not None
    return combined
