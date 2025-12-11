import yfinance as yf
import pandas as pd

def get_price_data(symbol: str, period: str) -> pd.DataFrame:
  return yf.download(symbol, period=period)

def get_symbol_history(symbol: str, period: str):
  symbol_data = yf.Ticker(symbol)
  return symbol_data.history(period=period)