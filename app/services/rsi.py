import pandas as pd

def compute_rsi(df: pd.DataFrame, period: int = 14) -> float:
  """
  RSIを計算して最新値を返す

  Parameters
  ----------
  df : pd.DataFrame
      'Close' カラムを持つ株価データ
  period : int
      RSI計算期間（デフォルト14日）

  Returns
  -------
  float
      最新日のRSI値
  """
  delta = df['Close'].diff()

  # 上昇分と下降分に分ける
  up = delta.clip(lower=0)
  down = -delta.clip(upper=0)

  # 移動平均を計算
  ma_up = up.rolling(period).mean()
  ma_down = down.rolling(period).mean()

  # RSI 計算
  rsi = 100 - (100 / (1 + ma_up / ma_down))

  return rsi.iloc[-1].values[0]  # 最新値を返す
