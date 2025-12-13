import yfinance as yf
import pandas as pd

def get_price_data(symbol: str, period: str) -> pd.DataFrame:
  return yf.download(symbol, period=period, auto_adjust=False)