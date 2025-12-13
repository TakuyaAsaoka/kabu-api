import math
import pandas as pd

from app.services.market_condition.divergence import compute_divergence
from tests.utils import make_symbol_history_dummy_df

dummy_symbol_history_df = make_symbol_history_dummy_df()

class TestComputeDivergence:
  def test_乖離率を正しく算出できる(self):
    end_date = dummy_symbol_history_df.index.max()
    start_date = end_date - pd.DateOffset(years=2)
    dummy_symbol_history_df_2y = dummy_symbol_history_df.loc[start_date:end_date, 'Close']

    current_series = dummy_symbol_history_df_2y.iloc[-1]
    current_price = float(current_series.iloc[0])
    median_series = dummy_symbol_history_df_2y.median()
    median = float(median_series.iloc[0])
    expected = (current_price - median) / median

    actual = compute_divergence(dummy_symbol_history_df)

    assert math.isclose(actual, expected, rel_tol=1e-9)