import pandas as pd

def compute_usd_jpy_m_avg_df(df: pd.DataFrame) -> pd.DataFrame:
  return df['Close'].resample("ME").mean()