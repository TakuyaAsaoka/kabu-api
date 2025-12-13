import pandas as pd

from app.services.market_condition.weak_yen_env_assess.usd_jpy_m_avg_df import compute_usd_jpy_m_avg_df
from tests.utils import make_yf_download_dummy_df

dummy_df = make_yf_download_dummy_df()

class TestComputeUSDJPYMAveDf:
  def test_月間平均を正しく算出できる(self):
    expected = dummy_df["Close"].resample('ME').mean()
    actual = compute_usd_jpy_m_avg_df(dummy_df)

    pd.testing.assert_frame_equal(actual, expected)