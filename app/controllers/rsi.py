from fastapi import APIRouter
from ..repositories.market_data import get_price_data
from ..services.rsi import compute_rsi
from ..services.scoring_market_condition import scoring_nikkei_momentum

router = APIRouter(prefix="/rsi", tags=["RSI"])

@router.get("/{ticker}")
def rsi(ticker: str, period: int = 14):
  df = get_price_data(ticker)
  computed_rsi = compute_rsi(df = df, period = period)
  scored_nikkei_momentum = scoring_nikkei_momentum(rsi = computed_rsi)
  return {
    "ticker": ticker,
    "period": period,
    "market_condition": {
      "nikkei_momentum": {
        "score": float(scored_nikkei_momentum),
        "computed_rsi": computed_rsi
      }
    }
  }
