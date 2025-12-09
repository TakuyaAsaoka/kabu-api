import yfinance as yf
import pandas as pd

def get_price_data(ticker: str, period: str = "5y") -> pd.DataFrame:
  return yf.download(ticker, period=period)

def get_usd_jpy_history(period: str = "5y"):
  usd_jpy = yf.Ticker("JPY=X")
  return usd_jpy.history(period=period)