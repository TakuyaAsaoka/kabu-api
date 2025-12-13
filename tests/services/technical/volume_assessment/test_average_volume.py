import pytest

from app.services.technical.volume_assessment.average_volume import compute_average_volume
from tests.utils import make_yf_download_dummy_df

dummy_download_df = make_yf_download_dummy_df()
n = 10

class TestComputeAverageVolume:
  def test_平均出来高を正しく算出できる(self):
    dummy_volume = dummy_download_df["Volume"]
    series = dummy_volume.rolling(window=n).mean().iloc[-1]
    expected = float(series.iloc[0])

    actual = compute_average_volume(dummy_download_df, n)

    assert actual == pytest.approx(expected)
    assert isinstance(actual, float)