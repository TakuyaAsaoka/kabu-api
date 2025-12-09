import pytest
import pandas as pd
from unittest.mock import patch, call, MagicMock
from app.repositories.market_data import get_price_data, get_usd_jpy_history
from tests.utils import make_yf_download_dummy_df, make_usd_jpy_dummy_df

dummy_ticker = "7203.T"
dummy_download_df = make_yf_download_dummy_df()
dummy_usd_jpy_df = make_usd_jpy_dummy_df()

class TestGetPriceData:
  @patch("app.repositories.market_data.yf.download")
  def test_取得したDataFrameを返す(self, mock_download):
    mock_download.return_value = dummy_download_df

    df = get_price_data(dummy_ticker)

    assert isinstance(df, pd.DataFrame)
    assert df.equals(dummy_download_df)

  @patch("app.repositories.market_data.yf.download")
  def test_正しい引数で実行される(self, mock_download):
    mock_download.return_value = dummy_download_df

    # デフォルトperiod
    get_price_data(dummy_ticker)
    mock_download.assert_called_once_with(dummy_ticker, period="5y")
    assert call(dummy_ticker, period="1y") not in mock_download.call_args_list

    # period=1y
    get_price_data(dummy_ticker, period="1y")
    assert call(dummy_ticker, period="1y") in mock_download.call_args_list

  @patch("app.repositories.market_data.yf.download")
  def test_例外が出た時エラーを返す(self, mock_download):
    mock_download.side_effect = Exception("API error")

    with pytest.raises(Exception) as e:
      get_price_data(dummy_ticker)
    assert str(e.value) == "API error"

class TestGetUsdJpyHistory:
  @patch("app.repositories.market_data.yf.Ticker")
  def test_取得したDataFrameを返す(self, mock_ticker):
    mock_instance = MagicMock()
    mock_instance.history.return_value = dummy_usd_jpy_df
    mock_ticker.return_value = mock_instance

    result = get_usd_jpy_history()

    assert isinstance(result, pd.DataFrame)
    assert result.equals(dummy_usd_jpy_df)

  @patch("app.repositories.market_data.yf.Ticker")
  def test_正しい引数で実行されている(self, mock_ticker):
    mock_instance = MagicMock()
    mock_ticker.return_value = mock_instance

    get_usd_jpy_history()

    mock_ticker.assert_called_once_with("JPY=X")
    mock_instance.history.assert_called_once_with(period="5y")

    mock_ticker.reset_mock()
    mock_instance.history.reset_mock()

    get_usd_jpy_history("1y")
    mock_ticker.assert_called_once_with("JPY=X")
    mock_instance.history.assert_called_once_with(period="1y")
