from src.analysis.confidence import ConfidenceResult
from src.analysis.state import (
    MarketState,
    determine_market_state,
)
from src.analysis.trend import TrendDirection


def make_confidence(score: float) -> ConfidenceResult:
    return ConfidenceResult(
        score=score,
        ema_distance_score=0.0,
        rsi_score=0.0,
        slope_score=0.0,
    )


def test_strong_uptrend_state() -> None:
    result = determine_market_state(
        direction=TrendDirection.UP,
        confidence=make_confidence(80.0),
    )

    assert result == MarketState.STRONG_UPTREND


def test_weak_uptrend_state() -> None:
    result = determine_market_state(
        direction=TrendDirection.UP,
        confidence=make_confidence(74.99),
    )

    assert result == MarketState.WEAK_UPTREND


def test_strong_downtrend_state() -> None:
    result = determine_market_state(
        direction=TrendDirection.DOWN,
        confidence=make_confidence(80.0),
    )

    assert result == MarketState.STRONG_DOWNTREND


def test_weak_downtrend_state() -> None:
    result = determine_market_state(
        direction=TrendDirection.DOWN,
        confidence=make_confidence(60.0),
    )

    assert result == MarketState.WEAK_DOWNTREND


def test_sideways_state_is_neutral() -> None:
    result = determine_market_state(
        direction=TrendDirection.SIDEWAYS,
        confidence=make_confidence(100.0),
    )

    assert result == MarketState.NEUTRAL