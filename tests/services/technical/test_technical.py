import pytest

from app.services.technical.technical import scoring_trend

@pytest.mark.parametrize("deviation_rate, expected", [
  # 境界値テスト
  (-25, 0.0),
  (0, 50.0),
  (25, 100.0),

  # 中間値テスト
  (10, 70.0),

  # 境界のすぐ外側
  (-25.1, 0.0),
  (0.1, 50.2),
  (24.9, 99.8),
  (25.1, 100.0),
])
def test_トレンドを正しく算出できる(deviation_rate, expected):
  result = scoring_trend(deviation_rate)
  assert result == pytest.approx(expected)