import pandas as pd

def compute_ma_n(data: pd.DataFrame, n: int) -> float:
  close = data["Close"]
  series = close.rolling(window=n).mean().iloc[-1]
  return float(series.iloc[0])