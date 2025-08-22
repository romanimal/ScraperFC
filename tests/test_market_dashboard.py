import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from market_dashboard.data_fetcher import fetch_market_data


def test_fetch_market_data_returns_expected_keys():
    data = fetch_market_data(["AAPL"])
    assert isinstance(data, list)
    assert data
    row = data[0]
    expected = {"ticker", "price", "percent_change", "percent_52w_high", "52w_range"}
    assert expected <= row.keys()
