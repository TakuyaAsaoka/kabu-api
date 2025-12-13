import numpy as np
import pandas as pd

def make_yf_download_dummy_df() -> pd.DataFrame:
  date_index = pd.date_range("2020-11-01", "2025-11-01", freq="B")  # B=BusinessDay

  symbol = "7203.T"
  n = len(date_index)
  np.random.seed(42)

  # 緩やかな上昇トレンド + ノイズ（float64）
  close = (np.linspace(104, 156, n) + np.random.normal(0, 0.3, n)).astype("float64")
  adjustment_factor = np.linspace(0.97, 1.0, n)
  adj_close = (close * adjustment_factor).astype("float64")
  open_ = (close + np.random.normal(0, 0.1, n)).astype("float64")
  high = (np.maximum(open_, close) + 0.3).astype("float64")
  low = (np.minimum(open_, close) - 0.3).astype("float64")
  volume = (np.random.randint(800_000, 1_200_000, n)).astype("int64")

  # ベースとなる DataFrame（Series の形）
  base = pd.DataFrame({
    "Adj Close": adj_close,
    "Close": close,
    "High": high,
    "Low": low,
    "Open": open_,
    "Volume": volume
  }, index=date_index).round(6)

  # 本物データ同様、「価格種別 × 銘柄」の列マルチインデックスに変換
  #   1) 列を第一階層=価格種別 ("Adj Close", "Close", "High", "Low", "Open", "Volume")
  #   2) 第二階層=銘柄 ('7203.T') にする
  arrays = [
    base.columns,                    # 第一階層（価格種別）
    [symbol] * len(base.columns),    # 第二階層（銘柄）
  ]

  columns = pd.MultiIndex.from_arrays(arrays, names=["Price", "Ticker"])

  # 価格種別を最初の軸に保ったまま、銘柄軸を追加（列数が増える）
  # DataFrame を列方向に広げる
  df = pd.DataFrame(
    np.column_stack([base[c] for c in base.columns]),
    index=base.index,
    columns=columns
  )
  df.index.name = "Date"

  return df