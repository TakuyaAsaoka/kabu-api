from app.repositories.market_data import get_symbol_history

dummy_ticker = "7203.T"

def compute_divergence() -> float:
  data = get_symbol_history(dummy_ticker, "2y")
  close_prices = data['Close']

  current_price = close_prices.iloc[-1]
  median = close_prices.median()

  divergence = (current_price - median) / median
  return divergence
