from pydantic import BaseModel

class CommonParameter(BaseModel):
  symbol: str
  period: str
  symbol_current_price: float

class NikkeiMomentum(BaseModel):
  score: float
  rsi: float

class WeakYenEnvAssess(BaseModel):
  score: float
  current_rate: float
  m_avg_median: float
  q10: float
  q90: float

class MarketCondition(BaseModel):
  nikkei_momentum: NikkeiMomentum
  weak_yen_env_assess: WeakYenEnvAssess

class Trend(BaseModel):
  score: float
  n: int
  ma_n: float
  deviation_rate: float

class ShortTermOverheatingAssess(BaseModel):
  score: float
  rsi: float

class VolumeAssess(BaseModel):
  score: float
  ave_vol_short: float
  ave_vol_long: float

class PriceBandVolumeAssess(BaseModel):
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
  short_term_overheating_assessment: ShortTermOverheatingAssess
  volume_assessment: VolumeAssess
  price_band_volume_assessment: PriceBandVolumeAssess

class ScoreResponse(BaseModel):
  common_parameter: CommonParameter
  market_condition: MarketCondition
  technical: Technical