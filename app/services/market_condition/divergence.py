import pandas as pd

def compute_divergence(data: pd.DataFrame) -> float:
  end_date = data.index.max()
  start_date = end_date - pd.DateOffset(years=2)
  close_prices_2y = data.loc[start_date:end_date, 'Close']

  current_price_series = close_prices_2y.iloc[-1]
  current_price = float(current_price_series.iloc[0])
  median_series = close_prices_2y.median()
  median = float(median_series.iloc[0])

  divergence = (current_price - median) / median
  return divergence
