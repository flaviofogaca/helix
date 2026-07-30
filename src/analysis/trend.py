from enum import Enum


class TrendDirection(Enum):
    UP = "UP"
    DOWN = "DOWN"
    SIDEWAYS = "SIDEWAYS"


def analyze_trend(
    ema20: float,
    ema50: float,
    tolerance: float = 0.0005,
) -> TrendDirection:
    """
    Classifica a direção estrutural usando a distância relativa
    entre EMA20 e EMA50.

    tolerance=0.0005 equivale a 0,05%.
    """

    if ema50 == 0:
        raise ValueError("EMA50 não pode ser zero.")

    relative_distance = (ema20 - ema50) / ema50

    if relative_distance > tolerance:
        return TrendDirection.UP

    if relative_distance < -tolerance:
        return TrendDirection.DOWN

    return TrendDirection.SIDEWAYS