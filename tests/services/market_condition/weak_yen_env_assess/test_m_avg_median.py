import numpy as np
import pytest

from app.services.market_condition.weak_yen_env_assess.m_avg_median import compute_m_avg_median
from app.services.market_condition.weak_yen_env_assess.usd_jpy_m_avg_df import compute_usd_jpy_m_avg_df
from tests.utils import make_yf_download_dummy_df

dummy_df = make_yf_download_dummy_df()
m_avg_df = compute_usd_jpy_m_avg_df(dummy_df)

class TestComputeMAvgMedian:
  def test_過去5年の月間平均レートの中央値を正しく算出できる(self):
    window_months = 60
    s = m_avg_df.dropna()
    last = s.iloc[-window_months:].values.astype(float)

    expected = float(np.median(last))
    actual = compute_m_avg_median(m_avg_df, window_months)

    assert actual == pytest.approx(expected)