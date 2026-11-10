"""The data contract the rest of the harness is written against.

Backtests most often go wrong by using information that was not available at
decision time. Rather than audit for that afterwards, the engine is given no
way to read ahead: it holds a :class:`PanelData` and can only call
:meth:`PanelData.as_of`, which slices up to and including a date.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import pandas as pd


@dataclass(frozen=True)
class PanelData:
    """A wide panel of per-symbol fields, indexed by date.

    Parameters
    ----------
    fields:
        Mapping from field name (``"close"``, ``"dividend_yield"``, ...) to a
        DataFrame indexed by date with one column per symbol. All frames must
        share the same index and columns.
    """

    fields: dict[str, pd.DataFrame]

    def __post_init__(self) -> None:
        if not self.fields:
            raise ValueError("PanelData needs at least one field")
        frames = list(self.fields.values())
        reference = frames[0]
        if not reference.index.is_monotonic_increasing:
            raise ValueError("PanelData index must be sorted ascending")
        for name, frame in self.fields.items():
            if not frame.index.equals(reference.index):
                raise ValueError(f"field {name!r} has a different index")
            if list(frame.columns) != list(reference.columns):
                raise ValueError(f"field {name!r} has different symbols")

    @property
    def dates(self) -> pd.DatetimeIndex:
        return next(iter(self.fields.values())).index

    @property
    def symbols(self) -> list[str]:
        return list(next(iter(self.fields.values())).columns)

    def field(self, name: str) -> pd.DataFrame:
        try:
            return self.fields[name]
        except KeyError:
            available = ", ".join(sorted(self.fields))
            raise KeyError(f"no field {name!r}; available: {available}") from None

    def as_of(self, date: pd.Timestamp) -> PanelData:
        """Everything known up to and including ``date``, and nothing after.

        This is the only way the engine is allowed to read data.
        """
        return PanelData({k: v.loc[:date] for k, v in self.fields.items()})


class PriceLoader(Protocol):
    """Anything that can produce a :class:`PanelData` for a universe."""

    def load(
        self,
        symbols: list[str],
        start: str | pd.Timestamp,
        end: str | pd.Timestamp,
    ) -> PanelData:
        ...
