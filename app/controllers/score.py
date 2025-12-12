from fastapi import APIRouter
from ..repositories.market_data import get_price_data
from ..schemas.score import ScoreResponse, MarketCondition, NikkeiMomentum, Technical, Trend, CommonParameter, \
  ShortTermOverheatingAssessment
from app.services.market_condition.rsi import compute_rsi
from app.services.market_condition.market_condition import scoring_nikkei_momentum
from ..services.technical.technical import scoring_trend, scoring_short_term_overheating_assessment
from ..services.technical.trend.deviation_rate import compute_deviation_rate
from ..services.technical.trend.ma_n import compute_ma_n

router = APIRouter(prefix="/score", tags=["Score"])

@router.get("/{symbol}", response_model=ScoreResponse)
def score_symbol(symbol: str, period: str) -> ScoreResponse:
  df = get_price_data(symbol, period)
  current_value = float(df["Close"].iloc[-1].item())

  common_parameter = CommonParameter(
    symbol=symbol,
    period=period,
    current_value=current_value
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
  trend_deviation_rate = compute_deviation_rate(current_value, trend_ma_n)
  trend_score = scoring_trend(trend_deviation_rate)

  short_term_overheating_assessment_score = scoring_short_term_overheating_assessment(computed_rsi)

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
    )
  )

  return ScoreResponse(
    common_parameter=common_parameter,
    market_condition=market_condition,
    technical=technical
  )
