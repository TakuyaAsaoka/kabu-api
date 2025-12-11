import math
from unittest.mock import patch

from app.services.market_condition.divergence import compute_divergence
from tests.utils import make_symbol_history_dummy_df

dummy_symbol_history_df = make_symbol_history_dummy_df()

class TestComputeDivergence:
  @patch("app.services.market_condition.divergence.get_symbol_history")
  def test_乖離率を正しく算出できる(self, mock_get_history):
    mock_get_history.return_value = dummy_symbol_history_df

    actual = compute_divergence()

    median = dummy_symbol_history_df['Close'].median()
    current = dummy_symbol_history_df['Close'].iloc[-1]
    expected = (current - median) / median

    assert math.isclose(actual, expected, rel_tol=1e-9)