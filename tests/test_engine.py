from src.analysis.engine import analyze_market
from src.analysis.state import MarketState
from src.analysis.trend import TrendDirection


def test_engine_strong_uptrend() -> None:
    result = analyze_market(
        ema20=101.0,
        ema50=100.0,
        rsi=65.0,
        ema20_previous=100.9,
    )

    assert result.direction == TrendDirection.UP
    assert result.confidence.score == 100.0
    assert result.state == MarketState.STRONG_UPTREND
    assert "forte tendência de alta" in result.explanation.title


def test_engine_strong_downtrend() -> None:
    result = analyze_market(
        ema20=99.0,
        ema50=100.0,
        rsi=35.0,
        ema20_previous=99.1,
    )

    assert result.direction == TrendDirection.DOWN
    assert result.confidence.score == 100.0
    assert result.state == MarketState.STRONG_DOWNTREND
    assert "forte tendência de baixa" in result.explanation.title


def test_engine_neutral_market() -> None:
    result = analyze_market(
        ema20=100.01,
        ema50=100.0,
        rsi=50.0,
        ema20_previous=100.0,
    )

    assert result.direction == TrendDirection.SIDEWAYS
    assert result.confidence.score == 0.0
    assert result.state == MarketState.NEUTRAL
    assert result.explanation.warning is not None


def test_downtrend_with_low_rsi_generates_warning() -> None:
    result = analyze_market(
        ema20=99.0,
        ema50=100.0,
        rsi=25.0,
        ema20_previous=99.1,
    )

    assert result.explanation.warning is not None
    assert "repique" in result.explanation.warning