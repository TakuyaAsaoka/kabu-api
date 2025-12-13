import numpy as np
import pytest

from app.services.market_condition.weak_yen_env_assess.q import compute_q
from app.services.market_condition.weak_yen_env_assess.usd_jpy_m_avg_df import compute_usd_jpy_m_avg_df
from tests.utils import make_yf_download_dummy_df

dummy_df = make_yf_download_dummy_df()
m_avg_df = compute_usd_jpy_m_avg_df(dummy_df)

class TestComputeQ:
  @pytest.mark.parametrize(
    "n",
    [
      10,
      90,
    ]
  )
  def test_過去5年のN分位を正しく算出できる(self, n):
    window_months = 60
    s = m_avg_df.dropna()
    last = s.iloc[-window_months:].values.astype(float)

    expected = float(np.percentile(last, n))
    actual = compute_q(m_avg_df, n, window_months)

    assert actual == pytest.approx(expected)