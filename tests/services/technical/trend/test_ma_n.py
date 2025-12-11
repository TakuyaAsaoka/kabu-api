import pytest

from app.services.technical.trend.ma_n import compute_ma_n
from tests.utils import make_symbol_history_dummy_df

# TODO: このダミーデータだと、.iloc[-1]の返り値の型がfloatになってしまい、本物データと挙動が違うため作り直したい
dummy_symbol_history_df = make_symbol_history_dummy_df()
n = 20

class TestComputeMAN:
  def test_MA_Nを正しく算出できる(self):
    dummy_close = dummy_symbol_history_df["Close"]
    expected = dummy_close.rolling(window=n).mean().iloc[-1]

    actual = compute_ma_n(dummy_symbol_history_df, n)

    assert actual == pytest.approx(expected)
    # TODO: floatにキャストせずとも通ってしまう
    # assert isinstance(actual, float)