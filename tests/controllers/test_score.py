from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.schemas.score import ScoreResponse, MarketCondition, NikkeiMomentum

client = TestClient(app)

@patch("app.controllers.score.scoring_nikkei_momentum")
@patch("app.controllers.score.compute_rsi")
@patch("app.controllers.score.get_price_data")
def test_score_tickerは200レスポンスと正しいbodyを返す(
  mock_get_price_data,
  mock_compute_rsi,
  mock_scoring
):
  ticker = "7203.T"

  mock_get_price_data.return_value = "dummy_df"
  mock_compute_rsi.return_value = 55.123
  mock_scoring.return_value = 37.5

  expected = ScoreResponse(
    ticker = ticker,
    market_condition = MarketCondition(
      nikkei_momentum = NikkeiMomentum(
        score = mock_scoring.return_value,
        computed_rsi = mock_compute_rsi.return_value
      )
    )
  )

  response = client.get(f"/score/{expected.ticker}")

  assert response.status_code == 200

  actual = ScoreResponse(**response.json())
  assert actual == expected
