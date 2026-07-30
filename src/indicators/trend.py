import pandas as pd


def ema(df: pd.DataFrame, period: int):
    return df["close"].ewm(span=period, adjust=False).mean()