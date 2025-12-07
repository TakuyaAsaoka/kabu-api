import yfinance as yf
import pandas as pd

def get_price_data(ticker: str, period: str = "5y") -> pd.DataFrame:
  return yf.download(ticker, period=period)
