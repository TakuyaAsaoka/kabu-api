from app.repositories.market_data import get_symbol_history

# TODO: tickerが固定されている...
dummy_ticker = "7203.T"

def compute_divergence() -> float:
  # TODO: 一度取得したhistoryから2yで切り出せるようにする
  data = get_symbol_history(dummy_ticker, "2y")
  close_prices = data['Close']

  current_price_series = close_prices.iloc[-1]
  current_price = float(current_price_series.iloc[0])
  median_series = close_prices.median()
  median = float(median_series.iloc[0])

  divergence = (current_price - median) / median
  return divergence
