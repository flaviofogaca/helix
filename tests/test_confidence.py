import pytest

from src.analysis.confidence import calculate_confidence
from src.analysis.trend import TrendDirection


def test_strong_uptrend_confidence() -> None:
    result = calculate_confidence(
        direction=TrendDirection.UP,
        ema20=101.0,
        ema50=100.0,
        rsi=65.0,
        ema20_previous=100.9,
    )

    assert result.score == 100.0
    assert result.ema_distance_score == 45.0
    assert result.rsi_score == 35.0
    assert result.slope_score == 20.0


def test_strong_downtrend_confidence() -> None:
    result = calculate_confidence(
        direction=TrendDirection.DOWN,
        ema20=99.0,
        ema50=100.0,
        rsi=35.0,
        ema20_previous=99.1,
    )

    assert result.score == 100.0
    assert result.ema_distance_score == 45.0
    assert result.rsi_score == 35.0
    assert result.slope_score == 20.0


def test_sideways_confidence_is_zero() -> None:
    result = calculate_confidence(
        direction=TrendDirection.SIDEWAYS,
        ema20=100.0,
        ema50=100.0,
        rsi=50.0,
        ema20_previous=100.0,
    )

    assert result.score == 0.0
    assert result.ema_distance_score == 0.0
    assert result.rsi_score == 0.0
    assert result.slope_score == 0.0


def test_invalid_rsi_raises_error() -> None:
    with pytest.raises(
        ValueError,
        match="RSI deve estar entre 0 e 100",
    ):
        calculate_confidence(
            direction=TrendDirection.UP,
            ema20=101.0,
            ema50=100.0,
            rsi=110.0,
            ema20_previous=100.9,
        )