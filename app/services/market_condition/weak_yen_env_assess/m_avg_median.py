import numpy as np
import pandas as pd

def compute_m_avg_median(df: pd.DataFrame, window_months: int) -> float:
  s = df.dropna()
  last = s.iloc[-window_months:].values.astype(float)
  return float(np.median(last))