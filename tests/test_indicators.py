import pandas as pd

from app.internal.analysis import indicators


def test_calculate_moving_averages():
    df = pd.DataFrame({"close": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
    result = indicators.calculate_moving_averages(df.copy())
    assert "5ma" in result.columns
    assert "10ma" in result.columns
    assert result["5ma"].iloc[4] == 3.0
    assert result["10ma"].iloc[9] == 5.5


def test_calculate_bollinger_bands():
    df = pd.DataFrame({"close": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
    result = indicators.calculate_bollinger_bands(df.copy(), window=5)
    assert "bollinger_upper" in result.columns
    assert "bollinger_lower" in result.columns
    assert result["bollinger_upper"].notnull().sum() > 0


def test_calculate_atr():
    df = pd.DataFrame({"high": [2, 3, 4], "low": [1, 2, 3], "close": [1.5, 2.5, 3.5]})
    result = indicators.calculate_atr(df.copy(), window=2)
    assert "atr" in result.columns
    assert result["atr"].notnull().sum() > 0


def test_calculate_rsi():
    df = pd.DataFrame({"close": [1, 2, 3, 2, 1, 2, 3, 4, 5, 6]})
    result = indicators.calculate_rsi(df.copy(), window=3)
    assert "rsi" in result.columns
    assert result["rsi"].notnull().sum() > 0


def test_calculate_macd():
    df = pd.DataFrame({"close": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
    result = indicators.calculate_macd(df.copy())
    assert "macd" in result.columns
    assert "signal_line" in result.columns


def test_calculate_vma():
    df = pd.DataFrame({"volume": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
    result = indicators.calculate_vma(df.copy())
    assert "vma_short" in result.columns
    assert "vma_long" in result.columns


def test_calculate_cci():
    df = pd.DataFrame(
        {"high": [2, 3, 4, 5], "low": [1, 2, 3, 4], "close": [1.5, 2.5, 3.5, 4.5]}
    )
    result = indicators.calculate_cci(df.copy(), window=2)
    assert "cci" in result.columns
    assert result["cci"].notnull().sum() > 0


def test_calculate_kdj():
    df = pd.DataFrame(
        {
            "high": [2, 3, 4, 5, 6],
            "low": [1, 2, 3, 4, 5],
            "close": [1.5, 2.5, 3.5, 4.5, 5.5],
        }
    )
    result = indicators.calculate_kdj(df.copy(), window=3)
    assert "kdj_k" in result.columns
    assert "kdj_d" in result.columns
    assert "kdj_j" in result.columns


def test_calculate_obv():
    df = pd.DataFrame({"close": [1, 2, 3, 2, 1], "volume": [10, 20, 30, 40, 50]})
    result = indicators.calculate_obv(df.copy())
    assert "obv" in result.columns
    # OBV calculation: [0, 20, 50, 10, -40]
    assert result["obv"].iloc[-1] == -40
