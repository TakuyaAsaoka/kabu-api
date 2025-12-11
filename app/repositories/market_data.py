import yfinance as yf
import pandas as pd

def get_price_data(ticker: str, period: str) -> pd.DataFrame:
  return yf.download(ticker, period=period)

def get_symbol_history(symbol: str, period: str):
  symbol_data = yf.Ticker(symbol)
  return symbol_data.history(period=period)