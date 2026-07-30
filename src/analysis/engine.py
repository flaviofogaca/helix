from dataclasses import dataclass

from src.analysis.confidence import (
    ConfidenceResult,
    calculate_confidence,
)
from src.analysis.explanation import (
    MarketExplanation,
    build_explanation,
)
from src.analysis.state import (
    MarketState,
    determine_market_state,
)
from src.analysis.trend import (
    TrendDirection,
    analyze_trend,
)


@dataclass(frozen=True)
class AnalysisResult:
    """
    Resultado completo da análise de mercado do Helix.
    """

    direction: TrendDirection
    confidence: ConfidenceResult
    state: MarketState
    explanation: MarketExplanation


def analyze_market(
    *,
    ema20: float,
    ema50: float,
    rsi: float,
    ema20_previous: float,
    trend_tolerance: float = 0.0005,
) -> AnalysisResult:
    """
    Executa o pipeline completo de análise do Helix.

    Pipeline:
        Trend
            ↓
        Confidence
            ↓
        Market State
            ↓
        Explanation
    """

    direction = analyze_trend(
        ema20=ema20,
        ema50=ema50,
        tolerance=trend_tolerance,
    )

    confidence = calculate_confidence(
        direction=direction,
        ema20=ema20,
        ema50=ema50,
        rsi=rsi,
        ema20_previous=ema20_previous,
    )

    state = determine_market_state(
        direction=direction,
        confidence=confidence,
    )

    explanation = build_explanation(
        direction=direction,
        confidence=confidence,
        state=state,
        ema20=ema20,
        ema50=ema50,
        rsi=rsi,
        ema20_previous=ema20_previous,
    )

    return AnalysisResult(
        direction=direction,
        confidence=confidence,
        state=state,
        explanation=explanation,
    )