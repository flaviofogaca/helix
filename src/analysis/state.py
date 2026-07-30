from enum import Enum

from src.analysis.confidence import ConfidenceResult
from src.analysis.trend import TrendDirection


STRONG_TREND_THRESHOLD = 75


class MarketState(str, Enum):
    """
    Estados possíveis do mercado na primeira versão do Helix.

    Esta camada não calcula indicadores nem toma decisões.
    Ela apenas representa o resultado final da análise.
    """

    STRONG_UPTREND = "strong_uptrend"
    WEAK_UPTREND = "weak_uptrend"
    NEUTRAL = "neutral"
    WEAK_DOWNTREND = "weak_downtrend"
    STRONG_DOWNTREND = "strong_downtrend"


def determine_market_state(
    direction: TrendDirection,
    confidence: ConfidenceResult,
) -> MarketState:
    """
    Converte direção + confiança em um estado do mercado.
    """

    if direction == TrendDirection.SIDEWAYS:
        return MarketState.NEUTRAL

    score = confidence.score

    if direction == TrendDirection.UP:
        if score >= STRONG_TREND_THRESHOLD:
            return MarketState.STRONG_UPTREND

        return MarketState.WEAK_UPTREND

    if direction == TrendDirection.DOWN:
        if score >= STRONG_TREND_THRESHOLD:
            return MarketState.STRONG_DOWNTREND

        return MarketState.WEAK_DOWNTREND

    return MarketState.NEUTRAL