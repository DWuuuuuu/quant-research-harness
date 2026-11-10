"""Tushare adapter for A-share data.

Credentials come from the ``TUSHARE_TOKEN`` environment variable and are never
read from a file in this repository, never written to a notebook cell, and
never logged. If the variable is unset the loader fails loudly rather than
falling back to anything.

Requires the optional dependency: ``pip install tushare``.
"""

from __future__ import annotations

import os
import time

import pandas as pd

from qrh.data.base import PanelData

TOKEN_ENV_VAR = "TUSHARE_TOKEN"


class TushareLoader:
    """Load daily A-share price and valuation data.

    Parameters
    ----------
    token:
        Overrides the environment variable. Provided for tests; prefer the
        environment variable in anything you run or share.
    pause:
        Seconds between API calls, to stay inside Tushare's rate limits.
    """

    def __init__(self, token: str | None = None, pause: float = 0.35) -> None:
        resolved = token or os.environ.get(TOKEN_ENV_VAR)
        if not resolved:
            raise RuntimeError(
                f"{TOKEN_ENV_VAR} is not set. Export it in your shell "
                f"(see .env.example); do not hard-code it."
            )
        try:
            import tushare as ts
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise ImportError("TushareLoader needs `pip install tushare`") from exc
        ts.set_token(resolved)
        self._api = ts.pro_api()
        self._pause = pause

    def load(
        self,
        symbols: list[str],
        start: str | pd.Timestamp,
        end: str | pd.Timestamp,
    ) -> PanelData:
        """Fetch ``close``, ``dividend_yield`` and ``earnings_yield`` per symbol.

        Prices are adjusted-close equivalents; valuation fields come from
        ``daily_basic``, which Tushare publishes point-in-time, so no
        restatement correction is applied here.
        """
        start_str = pd.Timestamp(start).strftime("%Y%m%d")
        end_str = pd.Timestamp(end).strftime("%Y%m%d")

        closes: dict[str, pd.Series] = {}
        div_yields: dict[str, pd.Series] = {}
        earn_yields: dict[str, pd.Series] = {}

        for symbol in symbols:
            price = self._api.daily(ts_code=symbol, start_date=start_str, end_date=end_str)
            basic = self._api.daily_basic(
                ts_code=symbol,
                start_date=start_str,
                end_date=end_str,
                fields="trade_date,dv_ttm,pe_ttm",
            )
            time.sleep(self._pause)

            price = price.assign(date=pd.to_datetime(price["trade_date"])).set_index("date")
            basic = basic.assign(date=pd.to_datetime(basic["trade_date"])).set_index("date")

            closes[symbol] = price["close"].sort_index()
            # Tushare reports dv_ttm in percent; convert to a fraction.
            div_yields[symbol] = (basic["dv_ttm"] / 100.0).sort_index()
            # Earnings yield rather than P/E, so that higher is always better
            # and the metric stays finite as earnings approach zero.
            earn_yields[symbol] = (1.0 / basic["pe_ttm"].replace(0.0, pd.NA)).sort_index()

        def align(series_by_symbol: dict[str, pd.Series]) -> pd.DataFrame:
            return pd.DataFrame(series_by_symbol).sort_index()

        close_frame = align(closes)
        index, columns = close_frame.index, close_frame.columns
        return PanelData(
            {
                "close": close_frame,
                "dividend_yield": align(div_yields)
                .reindex(index=index, columns=columns)
                .ffill(),
                "earnings_yield": align(earn_yields)
                .reindex(index=index, columns=columns)
                .ffill(),
            }
        )
