from app.repositories.market_data import get_usd_jpy_history

def compute_divergence() -> float:
  data = get_usd_jpy_history()
  close_prices = data['Close']

  current_price = close_prices.iloc[-1]
  median = close_prices.median()

  divergence = (current_price - median) / median
  return divergence
