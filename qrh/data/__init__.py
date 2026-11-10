"""Data access, with point-in-time discipline enforced at the boundary.

Every loader returns a :class:`~qrh.data.base.PanelData` object. The engine
only ever asks it for data *as of* a date, so a look-ahead bug has to be
written deliberately rather than by accident.
"""

from qrh.data.base import PanelData, PriceLoader
from qrh.data.synthetic import SyntheticLoader

__all__ = ["PanelData", "PriceLoader", "SyntheticLoader"]
