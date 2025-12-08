
import pytest
from app.controllers.score import scoring_nikkei_momentum

# 複数のテストケースを一括で定義するためのpytestの機能
@pytest.mark.parametrize("rsi, expected", [
  # 境界値テスト
  (70, 100.0),       # RSI >= 70 → 100
  (80, 100.0),       # RSI > 70 → 100
  (50, 50.0),        # RSI == 50 → 50
  (30, 0.0),         # RSI <= 30 → 0
  (20, 0.0),         # RSI < 30 → 0

  # 中間値テスト
  (60, 50 + (60 - 50) * 2.5),  # 50 < RSI < 70 → 50 + (RSI - 50) * 2.5
  (40, 50 + (40 - 50) * 1.5),  # 30 < RSI < 50 → 50 + (RSI - 50) * 1.5

  # 境界のすぐ外側
  (69.9, 50 + (69.9 - 50) * 2.5),
  (30.1, 50 + (30.1 - 50) * 1.5),
])
def test_scoring_nikkei_momentum(rsi, expected):
  result = scoring_nikkei_momentum(rsi)
  assert result == pytest.approx(expected)
