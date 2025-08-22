"""Utilities to fetch market data."""

from __future__ import annotations

from typing import Iterable, List, Dict

import pandas as pd
import yfinance as yf

DEFAULT_TICKERS = ["AAPL", "MSFT", "GOOG", "AMZN", "META"]


def fetch_market_data(tickers: Iterable[str] | None = None) -> List[Dict[str, float]]:
    """Return market metrics for the given tickers.

    Parameters
    ----------
    tickers: Iterable[str] | None
        Symbols to fetch. If ``None`` the ``DEFAULT_TICKERS`` are used.
    """
    tickers = list(tickers) if tickers is not None else DEFAULT_TICKERS
    results: List[Dict[str, float]] = []
    for symbol in tickers:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1y")
        if hist.empty:
            continue
        last_close = hist["Close"].iloc[-1]
        prev_close = hist["Close"].iloc[-2] if len(hist) > 1 else last_close
        change_pct = ((last_close - prev_close) / prev_close) * 100 if prev_close else 0.0
        high_52 = hist["Close"].max()
        low_52 = hist["Close"].min()
        pct_52_high = (last_close / high_52) * 100 if high_52 else 0.0
        results.append(
            {
                "ticker": symbol,
                "price": round(float(last_close), 2),
                "percent_change": round(float(change_pct), 2),
                "percent_52w_high": round(float(pct_52_high), 2),
                "52w_range": f"{round(float(low_52),2)} - {round(float(high_52),2)}",
            }
        )
    return results
