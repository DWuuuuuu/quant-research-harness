"""Cross-sectional indicators.

Each is a pure function of a :class:`~qrh.data.base.PanelData` slice returning
one score per symbol, higher meaning more attractive. The research inventory
these implement is in ``docs/indicators``.
"""

from qrh.indicators.base import Indicator
from qrh.indicators.carry import dividend_yield
from qrh.indicators.momentum import momentum, risk_adjusted_momentum
from qrh.indicators.value import earnings_yield
from qrh.indicators.volatility import inverse_volatility

__all__ = [
    "Indicator",
    "dividend_yield",
    "earnings_yield",
    "inverse_volatility",
    "momentum",
    "risk_adjusted_momentum",
]
