from app.services.rsi import compute_rsi
from tests.utils import make_dummy_yf_download_dummy_data

dummy_df = make_dummy_yf_download_dummy_data()

class TestComputeRSI:
  def test_floatを返す(self):
    result = compute_rsi(dummy_df)

    assert isinstance(result, float)
    assert 0 <= result <= 100