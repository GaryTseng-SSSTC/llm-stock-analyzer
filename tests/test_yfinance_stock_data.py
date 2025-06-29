from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from app.internal.yfinance import stock_data


def test_fetch_kline_data_success():
    # Mock yfinance.download to return a valid DataFrame
    mock_df = pd.DataFrame(
        {"Open": [100], "High": [110], "Low": [90], "Close": [105], "Volume": [10000]}
    )
    with patch("yfinance.download", return_value=mock_df):
        df = stock_data.fetch_kline_data("2330.TW")
        assert not df.empty
        assert list(df.columns) == ["open", "high", "low", "close", "volume"]
        assert df["open"].iloc[0] == 100
        assert df["volume"].iloc[0] == 10  # 10000 // 1000


def test_fetch_kline_data_empty():
    with patch("yfinance.download", return_value=pd.DataFrame()):
        df = stock_data.fetch_kline_data("2330.TW")
        assert df.empty


def test_fetch_kline_data_missing_columns():
    # DataFrame missing 'Open' column
    mock_df = pd.DataFrame(
        {"High": [110], "Low": [90], "Close": [105], "Volume": [10000]}
    )
    with patch("yfinance.download", return_value=mock_df):
        df = stock_data.fetch_kline_data("2330.TW")
        assert df.empty


def test_fetch_kline_data_exception():
    with patch("yfinance.download", side_effect=Exception("API error")):
        df = stock_data.fetch_kline_data("2330.TW")
        assert df.empty


def test_fetch_stock_info_success():
    mock_info = {"sector": "Tech", "industry": "Semiconductors"}
    mock_ticker = MagicMock()
    mock_ticker.info = mock_info
    with patch("yfinance.Ticker", return_value=mock_ticker):
        info = stock_data.fetch_stock_info("2330.TW")
        assert info["sector"] == "Tech"
        assert info["industry"] == "Semiconductors"


def test_fetch_stock_info_missing_fields():
    mock_info = {}
    mock_ticker = MagicMock()
    mock_ticker.info = mock_info
    with patch("yfinance.Ticker", return_value=mock_ticker):
        info = stock_data.fetch_stock_info("2330.TW")
        assert info["sector"] == "未知行業"
        assert info["industry"] == "未知產業"


def test_fetch_stock_info_exception():
    with patch("yfinance.Ticker", side_effect=Exception("API error")):
        info = stock_data.fetch_stock_info("2330.TW")
        assert info["sector"] == "未知行業"
        assert info["industry"] == "未知產業"
