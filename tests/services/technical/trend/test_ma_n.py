import pytest

from app.services.technical.trend.ma_n import compute_ma_n
from tests.utils import make_symbol_history_dummy_df

dummy_symbol_history_df = make_symbol_history_dummy_df()
n = 20

class TestComputeMA:
  def test_MA_Nを正しく算出できる(self):
    dummy_close = dummy_symbol_history_df["Close"]
    expected = dummy_close.rolling(window=n).mean().iloc[-1]

    actual = compute_ma_n(dummy_symbol_history_df, n)

    assert actual == pytest.approx(expected)