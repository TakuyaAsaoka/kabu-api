# 1.地合い
# 1 日経平均モメンタム評価

def scoring_nikkei_momentum(rsi: float) -> float:
  """
  RSIの値を0〜100のスコアに変換する関数

  ルール：
  - RSI >= 70 → 100
  - 50 < RSI < 70 → 50 + (RSI - 50) * 2.5
  - RSI == 50 → 50
  - 30 < RSI < 50 → 50 + (RSI - 50) * 1.5
  - RSI <= 30 → 0
  """
  if rsi >= 70:
    return 100.0
  elif 50 < rsi < 70:
    return 50 + (rsi - 50) * 2.5
  elif rsi == 50:
    return 50.0
  elif 30 < rsi < 50:
    return 50 + (rsi - 50) * 1.5
  else:
    return 0.0

# 2 為替環境評価(円安)
def scoring_weak_yen_env_assess(current_rate: float, m_avg_median: float, q10: float, q90: float):
  if current_rate >= m_avg_median:
    s = 50 + (current_rate - m_avg_median) * (50 / (q90 - m_avg_median))
  else:
    s = 50 - (m_avg_median - current_rate) * (50 / (m_avg_median - q10))
  return max(0.0, min(100.0, s))
