from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.schemas.score import ScoreResponse, MarketCondition, NikkeiMomentum, CommonParameter, Technical, Trend, \
  ShortTermOverheatingAssessment, VolumeAssessment, PriceBandVolumeAssessment
from tests.utils import make_yf_download_dummy_df

client = TestClient(app)

@patch("app.controllers.score.compute_price_band_volume_ratio")
@patch("app.controllers.score.scoring_price_band_volume_assessment")
@patch("app.controllers.score.compute_average_volume")
@patch("app.controllers.score.scoring_volume_assessment")
@patch("app.controllers.score.scoring_short_term_overheating_assessment")
@patch("app.controllers.score.scoring_trend")
@patch("app.controllers.score.compute_deviation_rate")
@patch("app.controllers.score.compute_ma_n")
@patch("app.controllers.score.scoring_nikkei_momentum")
@patch("app.controllers.score.compute_rsi")
@patch("app.controllers.score.get_price_data")
def test_score_tickerは200レスポンスと正しいbodyを返す(
  mock_get_price_data,
  mock_compute_rsi,
  mock_scoring_nikkei_momentum,
  mock_compute_ma_n,
  mock_compute_deviation_rate,
  mock_scoring_trend,
  mock_scoring_short_term_overheating_assessment,
  mock_scoring_volume_assessment,
  mock_compute_average_volume,
  mock_scoring_price_band_volume_assessment,
  mock_compute_price_band_volume_ratio
):
  symbol = "7203.T"
  period = "5y"

  mock_get_price_data.return_value = make_yf_download_dummy_df()
  mock_compute_rsi.return_value = 55.123
  mock_scoring_nikkei_momentum.return_value = 37.5

  trend_weight = 0.4
  short_term_overheating_assessment_weight = 0.2
  volume_assessment_weight = 0.2
  price_band_volume_assessment_weight = 0.2

  mock_compute_ma_n.return_value = 2203.12
  mock_compute_deviation_rate.return_value = 13.0
  mock_scoring_trend.return_value = 58.45
  mock_scoring_short_term_overheating_assessment.return_value = 43.1

  mock_compute_average_volume.return_value = 10
  mock_scoring_volume_assessment.return_value = 82.4

  band_ratio=0.05
  mock_compute_price_band_volume_ratio.return_value = 0.21
  mock_scoring_price_band_volume_assessment.return_value = 30.8

  technical_score = (
    mock_scoring_trend.return_value * trend_weight +
    mock_scoring_short_term_overheating_assessment.return_value * short_term_overheating_assessment_weight +
    mock_scoring_volume_assessment.return_value * volume_assessment_weight +
    mock_scoring_price_band_volume_assessment.return_value * price_band_volume_assessment_weight
  )

  expected = ScoreResponse(
    common_parameter=CommonParameter(
      symbol= symbol,
      period=period,
      current_value=mock_get_price_data.return_value["Close"].iloc[-1].item()
    ),
    market_condition = MarketCondition(
      nikkei_momentum = NikkeiMomentum(
        score = mock_scoring_nikkei_momentum.return_value,
        rsi = mock_compute_rsi.return_value
      )
    ),
    technical=Technical(
      score=technical_score,
      trend_weight=trend_weight,
      short_term_overheating_assessment_weight=short_term_overheating_assessment_weight,
      volume_assessment_weight=volume_assessment_weight,
      price_band_volume_assessment_weight=price_band_volume_assessment_weight,
      trend=Trend(
        score=mock_scoring_trend.return_value,
        n=200,
        ma_n=mock_compute_ma_n.return_value,
        deviation_rate=mock_compute_deviation_rate.return_value
      ),
      short_term_overheating_assessment=ShortTermOverheatingAssessment(
        score=mock_scoring_short_term_overheating_assessment.return_value,
        rsi=mock_compute_rsi.return_value
      ),
      volume_assessment=VolumeAssessment(
        score=mock_scoring_volume_assessment.return_value,
        ave_vol_short=mock_compute_average_volume.return_value,
        ave_vol_long=mock_compute_average_volume.return_value,
      ),
      price_band_volume_assessment=PriceBandVolumeAssessment(
        score=mock_scoring_price_band_volume_assessment.return_value,
        price_band_volume_ratio=mock_compute_price_band_volume_ratio.return_value,
        band_ratio=band_ratio
      )
    )
  )

  response = client.get(f"/score/{expected.common_parameter.symbol}?period={expected.common_parameter.period}")

  assert response.status_code == 200

  actual = ScoreResponse(**response.json())
  assert actual == expected