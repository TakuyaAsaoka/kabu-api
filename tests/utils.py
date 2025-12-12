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

def make_symbol_history_dummy_df(symbol="7203.T") -> pd.DataFrame:
  # 営業日ベースの日付
  dates = pd.date_range("2025-11-01", "2025-11-30", freq="B")
  n = len(dates)
  np.random.seed(42)

  # 緩やかな上昇トレンド + ノイズ（float64）
  close = (np.linspace(104, 156, n) + np.random.normal(0, 0.3, n)).astype("float64")
  open_ = (close + np.random.normal(0, 0.1, n)).astype("float64")
  high = (np.maximum(open_, close) + 0.3).astype("float64")
  low = (np.minimum(open_, close) - 0.3).astype("float64")

  # ベースとなる DataFrame（Series の形）
  base = pd.DataFrame({
    "Open": open_,
    "High": high,
    "Low": low,
    "Close": close,
    "Volume": np.zeros(n, dtype="int64"),
    "Dividends": np.zeros(n, dtype="float64"),
    "Stock Splits": np.zeros(n, dtype="float64"),
  }, index=dates).round(6)

  # 本物データ同様、「価格種別 × 銘柄」の列マルチインデックスに変換
  #   1) 列を第一階層=価格種別 ('Open','High','Low','Close','Volume','Dividends','Stock Splits')
  #   2) 第二階層=銘柄 ('7203.T') にする
  arrays = [
    base.columns,                    # 第一階層（価格種別）
    [symbol] * len(base.columns),    # 第二階層（銘柄）
  ]
  columns = pd.MultiIndex.from_arrays(arrays, names=["Price", "Ticker"])
  # 価格種別を最初の軸に保ったまま、銘柄軸を追加（列数が増える）
  # DataFrame を列方向に広げる
  dummy_df = pd.DataFrame(
    np.column_stack([base[c] for c in base.columns]),
    index=base.index,
    columns=columns
  )

  return dummy_df