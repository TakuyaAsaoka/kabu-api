import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@patch("app.controllers.score.get_price_data")
@patch("app.controllers.score.compute_rsi")
@patch("app.controllers.score.scoring_nikkei_momentum")
def test_score_tickerは200レスポンスと正しいbodyを返す(mock_scoring, mock_compute_rsi, mock_get_price_data):
  mock_get_price_data.return_value = "dummy_df"
  mock_compute_rsi.return_value = 55.123
  mock_scoring.return_value = 37.5

  response = client.get("/score/7203.T")

  assert response.status_code == 200
  data = response.json()

  assert data["ticker"] == "7203.T"
  assert data["market_condition"]["nikkei_momentum"]["computed_rsi"] == mock_compute_rsi.return_value
  assert data["market_condition"]["nikkei_momentum"]["score"] == mock_scoring.return_value
