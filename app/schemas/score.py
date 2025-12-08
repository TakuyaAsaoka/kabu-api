from pydantic import BaseModel

class NikkeiMomentum(BaseModel):
  score: float
  computed_rsi: float

class MarketCondition(BaseModel):
  nikkei_momentum: NikkeiMomentum

class ScoreResponse(BaseModel):
  ticker: str
  market_condition: MarketCondition
