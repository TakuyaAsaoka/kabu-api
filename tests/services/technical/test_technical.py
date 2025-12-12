import pytest

from app.services.technical.technical import scoring_trend, scoring_short_term_overheating_assessment


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
  actual = scoring_trend(deviation_rate)
  assert actual == pytest.approx(expected)

@pytest.mark.parametrize("rsi, expected", [
  (50, 100.0),     # 中立 → 最大
  (40, 100 - (10**2)/20),  # RSI 40
  (60, 100 - (10**2)/20),  # RSI 60
  (0,  max(0, 100 - (50**2)/20)),   # 下限
  (100, max(0, 100 - (50**2)/20)),  # 上限
])
def test_短期過熱感評価を正しく算出できる(rsi, expected):
  actual = scoring_short_term_overheating_assessment(rsi)
  assert actual == pytest.approx(expected)
