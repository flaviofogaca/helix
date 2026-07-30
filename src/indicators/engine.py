"""
Indicator Engine

Responsável por calcular todos os indicadores utilizados pelo Helix.

Não contém regras de decisão.
"""

from src.indicators.trend import ema
from src.indicators.momentum import rsi

def calculate_indicators(df):

    df["EMA20"] = ema(df, 20)
    df["EMA50"] = ema(df, 50)
    df["RSI"] = rsi(df)

    return df