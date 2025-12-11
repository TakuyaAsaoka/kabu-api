import pytest

from app.services.technical.trend.deviation_rate import compute_deviation_rate

dummy_current_value = 1502.1
dummy_ma_n = 2124.3

class TestComputeDeviationRate:
  def test_乖離率を正しく算出できる(self):
    expected = (dummy_current_value - dummy_ma_n) / dummy_ma_n * 100

    actual = compute_deviation_rate(dummy_current_value, dummy_ma_n)

    assert actual == pytest.approx(expected)