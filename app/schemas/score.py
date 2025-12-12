from pydantic import BaseModel

class CommonParameter(BaseModel):
  symbol: str
  period: str
  current_value: float

class NikkeiMomentum(BaseModel):
  score: float
  rsi: float

class MarketCondition(BaseModel):
  nikkei_momentum: NikkeiMomentum

class Trend(BaseModel):
  score: float
  n: int
  ma_n: float
  deviation_rate: float

class ShortTermOverheatingAssessment(BaseModel):
  score: float
  rsi: float

class Technical(BaseModel):
  trend: Trend
  short_term_overheating_assessment: ShortTermOverheatingAssessment

class ScoreResponse(BaseModel):
  common_parameter: CommonParameter
  market_condition: MarketCondition
  technical: Technical