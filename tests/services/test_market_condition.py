import math
from unittest.mock import patch

import pytest
from app.controllers.score import scoring_nikkei_momentum
from app.services.market_condition import scoring_exchange_rate_assessment_yen_depreciation
from tests.utils import make_usd_jpy_dummy_df

dummy_usd_jpy_df = make_usd_jpy_dummy_df()

# 複数のテストケースを一括で定義するためのpytestの機能
@pytest.mark.parametrize("rsi, expected", [
  # 境界値テスト
  (70, 100.0),       # RSI >= 70 → 100
  (80, 100.0),       # RSI > 70 → 100
  (50, 50.0),        # RSI == 50 → 50
  (30, 0.0),         # RSI <= 30 → 0
  (20, 0.0),         # RSI < 30 → 0

  # 中間値テスト
  (60, 50 + (60 - 50) * 2.5),  # 50 < RSI < 70 → 50 + (RSI - 50) * 2.5
  (40, 50 + (40 - 50) * 1.5),  # 30 < RSI < 50 → 50 + (RSI - 50) * 1.5

  # 境界のすぐ外側
  (69.9, 50 + (69.9 - 50) * 2.5),
  (30.1, 50 + (30.1 - 50) * 1.5),
])
def test_scoring_nikkei_momentum(rsi, expected):
  result = scoring_nikkei_momentum(rsi)
  assert result == pytest.approx(expected)

@patch("app.services.market_condition.get_usd_jpy_history")
def test_為替環境評価を正しく算出できる(mock_get_history):
  mock_get_history.return_value = dummy_usd_jpy_df

  actual = scoring_exchange_rate_assessment_yen_depreciation()

  median = dummy_usd_jpy_df['Close'].median()
  current = dummy_usd_jpy_df['Close'].iloc[-1]
  expected = (current - median) / median

  assert math.isclose(actual, expected, rel_tol=1e-9)