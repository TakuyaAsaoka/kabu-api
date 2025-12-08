import pytest
import pandas as pd
from unittest.mock import patch, call
from app.repositories.market_data import get_price_data

dummy_ticker = "7203.T"
dummy_df = pd.DataFrame({"Close": [100, 101, 102]})

class TestGetPriceData:
  @patch("app.repositories.market_data.yf.download")
  def test_取得したDataFrameを返す(self, mock_download):
    mock_download.return_value = dummy_df

    df = get_price_data(dummy_ticker)

    assert isinstance(df, pd.DataFrame)
    assert df.equals(dummy_df)

  @patch("app.repositories.market_data.yf.download")
  def test_正しい引数で実行される(self, mock_download):
    mock_download.return_value = dummy_df

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
