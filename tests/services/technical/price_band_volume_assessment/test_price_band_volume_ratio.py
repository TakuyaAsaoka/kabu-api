import pytest

from app.services.technical.price_band_volume_assessment.price_band_volume_ratio import compute_price_band_volume_ratio
from tests.utils import make_yf_download_dummy_df

dummy_download_df = make_yf_download_dummy_df()
current_price = 2341.3
band_ratio = 0.05

class TestComputePriceBandVolumeRatio:
  def test_価格帯出来高比率を正しく算出できる(self):
    lower_price = current_price * (1 - band_ratio)

    band_df = dummy_download_df[
      (dummy_download_df["Close"] >= lower_price) &
      (dummy_download_df["Close"] <= current_price)
      ]

    band_volume = band_df["Volume"].sum()
    total_volume = dummy_download_df["Volume"].sum()

    series = band_volume / total_volume
    expected = float(series.iloc[0])

    actual = compute_price_band_volume_ratio(dummy_download_df, current_price, band_ratio)

    assert actual == pytest.approx(expected)
    assert isinstance(actual, float)