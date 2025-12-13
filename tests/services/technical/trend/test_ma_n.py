import pytest

from app.services.technical.trend.ma_n import compute_ma_n
from tests.utils import make_yf_download_dummy_df

dummy_df = make_yf_download_dummy_df()
n = 200

class TestComputeMAN:
  def test_MA_Nを正しく算出できる(self):
    dummy_close = dummy_df["Close"]
    series = dummy_close.rolling(window=n).mean().iloc[-1]
    expected = float(series.iloc[0])

    actual = compute_ma_n(dummy_df, n)

    assert actual == pytest.approx(expected)
    assert isinstance(actual, float)