from fastapi import APIRouter
from ..repositories.market_data import get_price_data
from ..schemas.score import ScoreResponse, MarketCondition, NikkeiMomentum, Technical, Trend, CommonParameter, \
  ShortTermOverheatingAssessment, VolumeAssessment, PriceBandVolumeAssessment
from app.services.market_condition.rsi import compute_rsi
from app.services.market_condition.market_condition import scoring_nikkei_momentum
from ..services.technical.price_band_volume_assessment.price_band_volume_ratio import compute_price_band_volume_ratio
from ..services.technical.technical import scoring_trend, scoring_short_term_overheating_assessment, \
  scoring_volume_assessment, scoring_price_band_volume_assessment
from ..services.technical.trend.deviation_rate import compute_deviation_rate
from ..services.technical.trend.ma_n import compute_ma_n
from ..services.technical.volume_assessment.average_volume import compute_average_volume

router = APIRouter(prefix="/score", tags=["Score"])

@router.get("/{symbol}", response_model=ScoreResponse)
def score_symbol(symbol: str, period: str) -> ScoreResponse:
  df = get_price_data(symbol, period)
  current_price = float(df["Close"].iloc[-1].item())

  common_parameter = CommonParameter(
    symbol=symbol,
    period=period,
    current_value=current_price
  )

  computed_rsi = compute_rsi(df = df)
  nikkei_momentum_score = scoring_nikkei_momentum(rsi = computed_rsi)
  market_condition = MarketCondition(
    nikkei_momentum=NikkeiMomentum(
      score=nikkei_momentum_score,
      rsi=computed_rsi
    )
  )

  trend_n = 200
  trend_ma_n = compute_ma_n(df, trend_n)
  trend_deviation_rate = compute_deviation_rate(current_price, trend_ma_n)
  trend_score = scoring_trend(trend_deviation_rate)

  short_term_overheating_assessment_score = scoring_short_term_overheating_assessment(computed_rsi)

  ave_vol_short = compute_average_volume(df, 5)
  ave_vol_long = compute_average_volume(df, 90)
  volume_assessment_score = scoring_volume_assessment(ave_vol_short, ave_vol_long)

  band_ratio = 0.05
  price_band_volume_ratio = compute_price_band_volume_ratio(df, current_price, band_ratio)
  price_band_volume_assessment_score = scoring_price_band_volume_assessment(price_band_volume_ratio)

  technical = Technical(
    trend=Trend(
      score=trend_score,
      n=trend_n,
      ma_n=trend_ma_n,
      deviation_rate=trend_deviation_rate
    ),
    short_term_overheating_assessment=ShortTermOverheatingAssessment(
      score=short_term_overheating_assessment_score,
      rsi=computed_rsi
    ),
    volume_assessment=VolumeAssessment(
      score=volume_assessment_score,
      ave_vol_short=ave_vol_short,
      ave_vol_long=ave_vol_long
    ),
    price_band_volume_assessment=PriceBandVolumeAssessment(
      score=price_band_volume_assessment_score,
      band_ratio=band_ratio,
      price_band_volume_ratio=price_band_volume_ratio
    )
  )

  return ScoreResponse(
    common_parameter=common_parameter,
    market_condition=market_condition,
    technical=technical
  )
