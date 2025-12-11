def compute_deviation_rate(current_value: float, ma_n: float) -> float:
  return (current_value - ma_n) / ma_n * 100