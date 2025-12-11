from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.schemas.score import ScoreResponse, MarketCondition, NikkeiMomentum, CommonParameter, Technical, Trend
from tests.utils import make_yf_download_dummy_df

client = TestClient(app)

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
  mock_scoring_trend
):
  symbol = "7203.T"
  period = "5y"

  mock_get_price_data.return_value = make_yf_download_dummy_df()
  mock_compute_rsi.return_value = 55.123
  mock_scoring_nikkei_momentum.return_value = 37.5

  mock_compute_ma_n.return_value = 2203.12
  mock_compute_deviation_rate.return_value = 13.0
  mock_scoring_trend.return_value = 58.45

  expected = ScoreResponse(
    common_parameter=CommonParameter(
      symbol= symbol,
      period=period,
      current_value=mock_get_price_data.return_value["Close"].iloc[-1].item()
    ),
    market_condition = MarketCondition(
      nikkei_momentum = NikkeiMomentum(
        score = mock_scoring_nikkei_momentum.return_value,
        computed_rsi = mock_compute_rsi.return_value
      )
    ),
    technical=Technical(
      trend=Trend(
        score=mock_scoring_trend.return_value,
        n=200,
        ma_n=mock_compute_ma_n.return_value,
        deviation_rate=mock_compute_deviation_rate.return_value
      )
    )
  )

  response = client.get(f"/score/{expected.common_parameter.symbol}?period={expected.common_parameter.period}")

  assert response.status_code == 200

  actual = ScoreResponse(**response.json())
  assert actual == expected
