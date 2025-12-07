from fastapi import APIRouter
from ..services.market_data import get_price_data
from ..indicators.rsi import compute_rsi

router = APIRouter(prefix="/rsi", tags=["RSI"])

@router.get("/{ticker}")
def rsi(ticker: str, period: int = 14):
  df = get_price_data(ticker)
  value = compute_rsi(df, period)
  return {"ticker": ticker, "period": period, "rsi": float(value)}
