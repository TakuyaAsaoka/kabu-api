import pytest
from app.controllers.score import scoring_nikkei_momentum
from app.services.market_condition.market_condition import scoring_weak_yen_env_assess


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
def test_日経平均モメンタムを正しく算出できる(rsi, expected):
  result = scoring_nikkei_momentum(rsi)
  assert result == pytest.approx(expected)

@pytest.mark.parametrize(
  "current_rate, m_avg_median, q10, q90, expected",
  [
    # 中央値と同じ → 50
    (145.0, 145.0, 140.0, 150.0, 50.0),
    # 中央値より上 → スコア計算 50～100
    (147.5, 145.0, 140.0, 150.0, 75.0),
    # 中央値より下 → スコア計算 0～50
    (142.5, 145.0, 140.0, 150.0, 25.0),
    # q10 より小さい → スコア下限 0 にクリップ
    (130.0, 145.0, 140.0, 150.0, 0.0),
    # q90 より大きい → スコア上限 100 にクリップ
    (155.0, 145.0, 140.0, 150.0, 100.0),
  ]
)
def test_為替環境評価を正しく算出できる(current_rate, m_avg_median, q10, q90, expected):
  score = scoring_weak_yen_env_assess(current_rate, m_avg_median, q10, q90)
  assert score == pytest.approx(expected)