import pandas as pd

def compute_ma_n(data: pd.DataFrame, n: int) -> float:
  close = data["Close"]
  # TODO: floatがテストできていない実装になっている
  return float(close.rolling(window=n).mean().iloc[-1])