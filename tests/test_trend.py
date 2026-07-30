import pytest

from src.analysis.trend import (
    TrendDirection,
    analyze_trend,
)


def test_analyze_trend_returns_up() -> None:
    result = analyze_trend(
        ema20=101.0,
        ema50=100.0,
    )

    assert result == TrendDirection.UP


def test_analyze_trend_returns_down() -> None:
    result = analyze_trend(
        ema20=99.0,
        ema50=100.0,
    )

    assert result == TrendDirection.DOWN


def test_analyze_trend_returns_sideways() -> None:
    result = analyze_trend(
        ema20=100.01,
        ema50=100.0,
    )

    assert result == TrendDirection.SIDEWAYS


def test_analyze_trend_rejects_zero_ema50() -> None:
    with pytest.raises(
        ValueError,
        match="EMA50 não pode ser zero",
    ):
        analyze_trend(
            ema20=100.0,
            ema50=0.0,
        )