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

# 2 短期過熱感評価
def scoring_short_term_overheating_assessment(rsi: float) -> float:
  return max(0.0, 100.0 - ((rsi - 50) ** 2) / 20)

# 3 出来高評価
def scoring_volume_assessment(ave_vol_short: float, ave_vol_long: float) -> float:
  score = 50.0 + ((ave_vol_short / ave_vol_long) - 1.0) * 50.0
  return max(0.0, min(100.0, score))