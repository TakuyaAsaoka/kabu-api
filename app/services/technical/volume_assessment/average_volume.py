import pandas as pd

def compute_average_volume(data: pd.DataFrame, n: int) -> float:
  volume = data["Volume"]
  series = volume.rolling(window=n).mean().iloc[-1]

  return float(series.iloc[0])

