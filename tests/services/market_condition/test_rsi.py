from app.services.market_condition.nikkei_momentum.rsi import compute_rsi
from tests.utils import make_yf_download_dummy_df

dummy_df = make_yf_download_dummy_df()

class TestComputeRSI:
  def test_floatを返す(self):
    result = compute_rsi(dummy_df)

    assert isinstance(result, float)
    assert 0 <= result <= 100