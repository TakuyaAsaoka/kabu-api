# 2.テクニカル
# 1 トレンド評価

def scoring_trend(deviation_rate: float) -> float:
  """
  ルール：
  - deviation_rate < -25 → 0
  - -25 <= deviation_rate <= 25 → 50 + (deviation_rate * 2)
  - 25 < deviation_rate → 100
  """
  if deviation_rate < -25:
    return 0.0
  elif 25 < deviation_rate:
    return 100.0
  else:
    return 50 + (deviation_rate * 2)
