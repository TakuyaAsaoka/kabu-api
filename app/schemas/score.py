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

class VolumeAssessment(BaseModel):
  score: float
  ave_vol_short: float
  ave_vol_long: float

class PriceBandVolumeAssessment(BaseModel):
  score: float
  price_band_volume_ratio: float
  band_ratio: float

class Technical(BaseModel):
  score: float
  trend_weight: float
  short_term_overheating_assessment_weight: float
  volume_assessment_weight: float
  price_band_volume_assessment_weight: float
  trend: Trend
  short_term_overheating_assessment: ShortTermOverheatingAssessment
  volume_assessment: VolumeAssessment
  price_band_volume_assessment: PriceBandVolumeAssessment

class ScoreResponse(BaseModel):
  common_parameter: CommonParameter
  market_condition: MarketCondition
  technical: Technical