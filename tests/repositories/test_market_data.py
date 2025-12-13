import pytest
import pandas as pd
from unittest.mock import patch
from app.repositories.market_data import get_price_data
from tests.utils import make_yf_download_dummy_df

dummy_ticker = "7203.T"
dummy_df = make_yf_download_dummy_df()

class TestGetPriceData:
  @patch("app.repositories.market_data.yf.download")
  def test_取得したDataFrameを返す(self, mock_download):
    mock_download.return_value = dummy_df

    df = get_price_data(dummy_ticker, "")

    assert isinstance(df, pd.DataFrame)
    assert df.equals(dummy_df)

  @patch("app.repositories.market_data.yf.download")
  def test_正しい引数で実行される(self, mock_download):
    mock_download.return_value = dummy_df

    get_price_data(dummy_ticker, "5y")
    mock_download.assert_called_once_with(dummy_ticker, period="5y", auto_adjust=False)

  @patch("app.repositories.market_data.yf.download")
  def test_例外が出た時エラーを返す(self, mock_download):
    mock_download.side_effect = Exception("API error")

    with pytest.raises(Exception) as e:
      get_price_data(dummy_ticker, "")
    assert str(e.value) == "API error"