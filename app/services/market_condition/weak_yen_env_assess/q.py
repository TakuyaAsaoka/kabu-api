import numpy as np
import pandas as pd

def compute_q(df: pd.DataFrame, n: int, window_months: int) -> float:
  s = df.dropna()
  last = s.iloc[-window_months:].values.astype(float)
  return float(np.percentile(last, n))