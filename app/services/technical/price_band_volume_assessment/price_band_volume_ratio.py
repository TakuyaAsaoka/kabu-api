import pandas as pd

def compute_price_band_volume_ratio(data: pd.DataFrame, current_price: float, band_ratio: float) -> float:
  lower_price = current_price * (1 - band_ratio)

  band_df = data[
    (data["Close"] >= lower_price) &
    (data["Close"] <= current_price)
  ]

  band_volume = band_df["Volume"].sum()
  total_volume = data["Volume"].sum()

  ratio = band_volume / total_volume

  return float(ratio.iloc[0])