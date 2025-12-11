import pandas as pd

def compute_ma_n(data: pd.DataFrame, n: int) -> float:
  close = data["Close"]
  return close.rolling(window=n).mean().iloc[-1]