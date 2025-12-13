import pytest

from app.services.technical.technical import scoring_trend, scoring_short_term_overheating_assessment, \
  scoring_volume_assessment, scoring_price_band_volume_assessment


@pytest.mark.parametrize("deviation_rate, expected", [
  # 境界値テスト
  (-25, 0.0),
  (0, 50.0),
  (25, 100.0),

  # 中間値テスト
  (10, 70.0),

  # 境界のすぐ外側
  (-25.1, 0.0),
  (0.1, 50.2),
  (24.9, 99.8),
  (25.1, 100.0),
])
def test_トレンドを正しく算出できる(deviation_rate, expected):
  actual = scoring_trend(deviation_rate)
  assert actual == pytest.approx(expected)

@pytest.mark.parametrize("rsi, expected", [
  (50, 100.0),     # 中立 → 最大
  (40, 100 - (10**2)/20),  # RSI 40
  (60, 100 - (10**2)/20),  # RSI 60
  (0,  max(0, 100 - (50**2)/20)),   # 下限
  (100, max(0, 100 - (50**2)/20)),  # 上限
])
def test_短期過熱感評価を正しく算出できる(rsi, expected):
  actual = scoring_short_term_overheating_assessment(rsi)
  assert actual == pytest.approx(expected)


@pytest.mark.parametrize("ave_vol_short, ave_vol_long, expected", [
  # 基準値
  (100, 100, 50.0),     # 出来高比率 = 1.0 → 50点

  # 上昇ケース
  (150, 100, 75.0),     # 1.5倍
  (200, 100, 100.0),    # 2.0倍 → 上限
  (300, 100, 100.0),    # 上限超過

  # 下降ケース
  (50, 100, 25.0),      # 0.5倍
  (0, 100, 0.0),        # 最小
])
def test_出来高評価を正しく算出できる(ave_vol_short, ave_vol_long, expected):
  result = scoring_volume_assessment(ave_vol_short, ave_vol_long)
  assert result == pytest.approx(expected)

@pytest.mark.parametrize(
  "price_band_volume_ratio, expected",
  [
    (0.0, 0.0),
    (0.01, 10.0),
    (0.1, 100.0),
    (1.0, 100.0),
  ]
)
def test_価格帯別出来高評価を正しく算出できる(price_band_volume_ratio, expected):
  result = scoring_price_band_volume_assessment(price_band_volume_ratio)
  assert result == pytest.approx(expected)