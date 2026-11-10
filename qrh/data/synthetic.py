"""A deterministic synthetic loader, so the repository runs with no credentials.

Every example in this repository runs against this loader by default. That is
deliberate: a reader can clone the repository and reproduce every number in
the README without a data vendor account, and the real adapters then swap in
behind the same interface.

The generator gives each symbol a persistent quality factor and a persistent
momentum factor, with noise large enough that naive strategies fail. It is not
a market simulator and should not be read as one.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from qrh.data.base import PanelData

TRADING_DAYS_PER_YEAR = 252


class SyntheticLoader:
    """Generate a reproducible synthetic panel.

    Parameters
    ----------
    seed:
        Fixed so that documented results stay reproducible.
    annual_drift, annual_vol:
        Market-wide parameters before cross-sectional effects.
    quality_spread:
        Annualised return spread between the best and worst symbol, which is
        what a cross-sectional strategy can in principle capture.
    """

    def __init__(
        self,
        seed: int = 20261110,
        annual_drift: float = 0.06,
        annual_vol: float = 0.22,
        quality_spread: float = 0.04,
    ) -> None:
        self.seed = seed
        self.annual_drift = annual_drift
        self.annual_vol = annual_vol
        self.quality_spread = quality_spread

    def load(
        self,
        symbols: list[str],
        start: str | pd.Timestamp,
        end: str | pd.Timestamp,
    ) -> PanelData:
        rng = np.random.default_rng(self.seed)
        dates = pd.bdate_range(start=start, end=end)
        n_dates, n_symbols = len(dates), len(symbols)
        if n_dates < 2 or n_symbols < 2:
            raise ValueError("need at least two dates and two symbols")

        daily_vol = self.annual_vol / np.sqrt(TRADING_DAYS_PER_YEAR)

        # Persistent per-symbol quality, evenly spaced so the spread is exact.
        quality = np.linspace(-0.5, 0.5, n_symbols) * self.quality_spread
        drift = (self.annual_drift + quality) / TRADING_DAYS_PER_YEAR

        # A common market factor plus idiosyncratic noise: without the common
        # factor, cross-sectional ranking looks far easier than it is.
        market = rng.normal(0.0, daily_vol * 0.7, size=(n_dates, 1))
        idio = rng.normal(0.0, daily_vol * 0.7, size=(n_dates, n_symbols))
        returns = drift + market + idio

        close = pd.DataFrame(
            100.0 * np.cumprod(1.0 + returns, axis=0), index=dates, columns=symbols
        )

        # Dividend yield correlates with quality but is noisy, so a yield
        # strategy is a degraded proxy for the quality factor rather than a
        # clean read on it.
        yield_base = 0.03 + quality * 0.5
        dividend_yield = pd.DataFrame(
            np.clip(
                yield_base + rng.normal(0.0, 0.004, size=(n_dates, n_symbols)),
                0.0,
                None,
            ),
            index=dates,
            columns=symbols,
        )

        earnings_yield = pd.DataFrame(
            np.clip(
                0.06 + quality + rng.normal(0.0, 0.012, size=(n_dates, n_symbols)),
                0.001,
                None,
            ),
            index=dates,
            columns=symbols,
        )

        return PanelData(
            {
                "close": close,
                "dividend_yield": dividend_yield,
                "earnings_yield": earnings_yield,
            }
        )
