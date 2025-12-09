import numpy as np
import pandas as pd

def make_yf_download_dummy_df() -> pd.DataFrame:
  # 期間インデックスを作成
  date_index = pd.date_range("2025-11-01", "2025-11-30", freq="B")  # B=BusinessDay

  ticker = "7203.T"
  price_kinds = ["Close", "High", "Low", "Open", "Volume"]

  # 階層付きの列名(MultiIndex)を作る
  cols = pd.MultiIndex.from_product(
    [price_kinds, [ticker]], # 列名を作成 ex. (Close, 7203.T), (High, 7203.T) のようなタプル
    names=["Price", "Ticker"] # 階層(一番左端列)の名前
  )

  n = len(date_index)

  # ---- 固定ルールで配列をそれぞれ作成 ----

  open_ = 3000 + np.cumsum(np.where(np.arange(n) % 2 == 0, +5, -5))
  close = open_ + np.where(np.arange(n) % 2 == 0, +2, -2)

  high    = np.maximum(open_, close) + 10          # 高値は +10
  low     = np.minimum(open_, close) - 10          # 安値は -10
  volume  = 2_000_000 + 20_000 * np.arange(n)      # 2,000,000, 2,020,000, ...

  # 列を横に並べて、2次元配列(行×列)を作る
  data = np.column_stack([close, high, low, open_, volume])

  # DataFrameを作る
  # 行インデックス: date_index
  # 列インデックス: cols(2階層の列名)
  df = pd.DataFrame(data, index=date_index, columns=cols)

  # インデックスに名前を付ける(正体はただの表示なだけで列ではない)
  df.index.name = "Date"

  # 型整形（価格はfloat(小数3桁)、出来高は整数）
  dummy_df = df.copy()
  for kind in ["Close", "High", "Low", "Open"]:
    dummy_df[(kind, ticker)] = dummy_df[(kind, ticker)].astype(float).round(3)
  dummy_df[("Volume", ticker)] = dummy_df[("Volume", ticker)].astype("Int64")

  return dummy_df

def make_usd_jpy_dummy_df() -> pd.DataFrame:
  dates = pd.date_range("2025-11-01", "2025-11-30", freq="B")
  n = len(dates)
  np.random.seed(42)

  # 緩やかな上昇トレンド + ノイズ
  close = np.linspace(104, 156, n) + np.random.normal(0, 0.3, n)
  open_ = close + np.random.normal(0, 0.1, n)
  high = np.maximum(open_, close) + 0.3
  low = np.minimum(open_, close) - 0.3

  dummy_df = pd.DataFrame({
    "Open": open_,
    "High": high,
    "Low": low,
    "Close": close,
    "Volume": 0,
    "Dividends": 0.0,
    "Stock Splits": 0.0,
  }, index=dates).round(6)

  return dummy_df