import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from app.repositories.market_data import get_price_data, get_symbol_history
from tests.utils import make_yf_download_dummy_df, make_symbol_history_dummy_df

dummy_ticker = "7203.T"
dummy_download_df = make_yf_download_dummy_df()
dummy_symbol_history_df = make_symbol_history_dummy_df()

class TestGetPriceData:
  @patch("app.repositories.market_data.yf.download")
  def test_取得したDataFrameを返す(self, mock_download):
    mock_download.return_value = dummy_download_df

    df = get_price_data(dummy_ticker, "")

    assert isinstance(df, pd.DataFrame)
    assert df.equals(dummy_download_df)

  @patch("app.repositories.market_data.yf.download")
  def test_正しい引数で実行される(self, mock_download):
    mock_download.return_value = dummy_download_df

    get_price_data(dummy_ticker, "5y")
    mock_download.assert_called_once_with(dummy_ticker, period="5y", auto_adjust=False)

  @patch("app.repositories.market_data.yf.download")
  def test_例外が出た時エラーを返す(self, mock_download):
    mock_download.side_effect = Exception("API error")

    with pytest.raises(Exception) as e:
      get_price_data(dummy_ticker, "")
    assert str(e.value) == "API error"

class TestGetSymbolHistory:
  @patch("app.repositories.market_data.yf.Ticker")
  def test_取得したDataFrameを返す(self, mock_ticker):
    mock_instance = MagicMock()
    mock_instance.history.return_value = dummy_symbol_history_df
    mock_ticker.return_value = mock_instance

    result = get_symbol_history(dummy_ticker, "")

    assert isinstance(result, pd.DataFrame)
    assert result.equals(dummy_symbol_history_df)

  @patch("app.repositories.market_data.yf.Ticker")
  def test_正しい引数で実行されている(self, mock_ticker):
    mock_instance = MagicMock()
    mock_ticker.return_value = mock_instance

    get_symbol_history(dummy_ticker, "5y")

    mock_ticker.assert_called_once_with(dummy_ticker)
    mock_instance.history.assert_called_once_with(period="5y")

  @patch("app.repositories.market_data.yf.Ticker")
  def test_yf_Tickerで例外が出た時エラーを返す(self, mock_ticker):
    mock_ticker.side_effect = Exception("Ticker error")

    with pytest.raises(Exception) as exc_info:
      get_symbol_history(dummy_ticker, "9999y")

    assert "Ticker error" in str(exc_info.value)

  @patch("app.repositories.market_data.yf.Ticker")
  def test_historyメソッドで例外が出た時エラーを返す(self, mock_ticker):
    mock_instance = MagicMock()
    mock_instance.history.side_effect = Exception("History error")
    mock_ticker.return_value = mock_instance

    with pytest.raises(Exception) as exc_info:
      get_symbol_history(dummy_ticker, "9999y")

    assert "History error" in str(exc_info.value)