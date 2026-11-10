"""yfinance adapter for US equities.

No credentials are needed. Requires the optional dependency:
``pip install yfinance``.
"""

from __future__ import annotations

import pandas as pd

from qrh.data.base import PanelData


class YFinanceLoader:
    """Load daily adjusted closes, with dividend yield derived from payouts.

    Valuation fields are deliberately *not* fetched from yfinance's snapshot
    endpoints: those report today's trailing P/E for every historical date,
    which is a look-ahead bug waiting to happen. Only ``close`` and a
    payout-derived ``dividend_yield`` are returned; anything fundamental
    should come from a point-in-time source such as EDGAR.
    """

    def load(
        self,
        symbols: list[str],
        start: str | pd.Timestamp,
        end: str | pd.Timestamp,
    ) -> PanelData:
        try:
            import yfinance as yf
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise ImportError("YFinanceLoader needs `pip install yfinance`") from exc

        raw = yf.download(
            tickers=symbols,
            start=pd.Timestamp(start),
            end=pd.Timestamp(end),
            auto_adjust=True,
            actions=True,
            progress=False,
            group_by="ticker",
        )
        if raw.empty:
            raise RuntimeError("yfinance returned no rows; check symbols and dates")

        closes, dividends = {}, {}
        for symbol in symbols:
            frame = raw[symbol] if isinstance(raw.columns, pd.MultiIndex) else raw
            closes[symbol] = frame["Close"]
            payouts = frame.get("Dividends", pd.Series(0.0, index=frame.index)).fillna(0.0)
            # Trailing twelve-month payouts over price, recomputed each day.
            dividends[symbol] = payouts.rolling(252, min_periods=1).sum() / frame["Close"]

        close_frame = pd.DataFrame(closes).sort_index().dropna(how="all")
        return PanelData(
            {
                "close": close_frame.ffill(),
                "dividend_yield": pd.DataFrame(dividends)
                .reindex(index=close_frame.index, columns=close_frame.columns)
                .fillna(0.0),
            }
        )
