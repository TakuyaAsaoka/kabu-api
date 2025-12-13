from fastapi import APIRouter
from ..repositories.market_data import get_price_data
from ..schemas.score import ScoreResponse, MarketCondition, NikkeiMomentum, Technical, Trend, CommonParameter, \
  ShortTermOverheatingAssess, VolumeAssess, PriceBandVolumeAssess, WeakYenEnvAssess
from app.services.market_condition.nikkei_momentum.rsi import compute_rsi
from app.services.market_condition.market_condition import scoring_nikkei_momentum, scoring_weak_yen_env_assess
from ..services.market_condition.weak_yen_env_assess.m_avg_median import compute_m_avg_median
from ..services.market_condition.weak_yen_env_assess.q import compute_q
from ..services.market_condition.weak_yen_env_assess.usd_jpy_m_avg_df import compute_usd_jpy_m_avg_df
from ..services.technical.price_band_volume_assessment.price_band_volume_ratio import compute_price_band_volume_ratio
from ..services.technical.technical import scoring_trend, scoring_short_term_overheating_assessment, \
  scoring_volume_assessment, scoring_price_band_volume_assessment
from ..services.technical.trend.deviation_rate import compute_deviation_rate
from ..services.technical.trend.ma_n import compute_ma_n
from ..services.technical.volume_assessment.average_volume import compute_average_volume

router = APIRouter(prefix="/score", tags=["Score"])

@router.get("/{symbol}", response_model=ScoreResponse)
def score_symbol(symbol: str, period: str) -> ScoreResponse:
  symbol_df = get_price_data(symbol, period)
  symbol_current_price = float(symbol_df["Close"].iloc[-1].item())
  usd_jpy_df = get_price_data("JPY=X", period)

  common_parameter = CommonParameter(
    symbol=symbol,
    period=period,
    symbol_current_price=symbol_current_price
  )

  rsi = compute_rsi(df = symbol_df)
  nikkei_momentum_score = scoring_nikkei_momentum(rsi = rsi)

  usd_jpy_m_avg_df = compute_usd_jpy_m_avg_df(usd_jpy_df)
  current_rate = float(usd_jpy_m_avg_df.iloc[-1, 0])
  m_avg_median = compute_m_avg_median(usd_jpy_m_avg_df, 60)
  q10 = compute_q(usd_jpy_m_avg_df, 10, 60)
  q90 = compute_q(usd_jpy_m_avg_df, 90, 60)
  weak_yen_env_assess_score = scoring_weak_yen_env_assess(current_rate, m_avg_median, q10, q90)

  market_condition = MarketCondition(
    nikkei_momentum=NikkeiMomentum(
      score=nikkei_momentum_score,
      rsi=rsi
    ),
    weak_yen_env_assess=WeakYenEnvAssess(
      score=weak_yen_env_assess_score,
      current_rate=current_rate,
      m_avg_median=m_avg_median,
      q10=q10,
      q90=q90
    )
  )

  trend_n = 200
  trend_ma_n = compute_ma_n(symbol_df, trend_n)
  trend_deviation_rate = compute_deviation_rate(symbol_current_price, trend_ma_n)
  trend_score = scoring_trend(trend_deviation_rate)

  short_term_overheating_assessment_score = scoring_short_term_overheating_assessment(rsi)

  ave_vol_short = compute_average_volume(symbol_df, 5)
  ave_vol_long = compute_average_volume(symbol_df, 90)
  volume_assessment_score = scoring_volume_assessment(ave_vol_short, ave_vol_long)

  band_ratio = 0.05
  price_band_volume_ratio = compute_price_band_volume_ratio(symbol_df, symbol_current_price, band_ratio)
  price_band_volume_assessment_score = scoring_price_band_volume_assessment(price_band_volume_ratio)

  trend_weight = 0.4
  short_term_overheating_assessment_weight = 0.2
  volume_assessment_weight = 0.2
  price_band_volume_assessment_weight = 0.2

  technical_score = (
    trend_score * trend_weight +
    short_term_overheating_assessment_score * short_term_overheating_assessment_weight +
    volume_assessment_score * volume_assessment_weight +
    price_band_volume_assessment_score * price_band_volume_assessment_weight
  )

  technical = Technical(
    score=technical_score,
    trend_weight=trend_weight,
    short_term_overheating_assessment_weight=short_term_overheating_assessment_weight,
    volume_assessment_weight=volume_assessment_weight,
    price_band_volume_assessment_weight=price_band_volume_assessment_weight,
    trend=Trend(
      score=trend_score,
      n=trend_n,
      ma_n=trend_ma_n,
      deviation_rate=trend_deviation_rate
    ),
    short_term_overheating_assessment=ShortTermOverheatingAssess(
      score=short_term_overheating_assessment_score,
      rsi=rsi
    ),
    volume_assessment=VolumeAssess(
      score=volume_assessment_score,
      ave_vol_short=ave_vol_short,
      ave_vol_long=ave_vol_long
    ),
    price_band_volume_assessment=PriceBandVolumeAssess(
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
