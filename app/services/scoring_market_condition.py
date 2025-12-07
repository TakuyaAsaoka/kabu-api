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