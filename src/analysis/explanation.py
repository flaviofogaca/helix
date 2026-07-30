from dataclasses import dataclass

from src.analysis.confidence import ConfidenceResult
from src.analysis.state import MarketState
from src.analysis.trend import TrendDirection


@dataclass(frozen=True)
class MarketExplanation:
    """
    Explicação textual da análise realizada pelo Helix.
    """

    title: str
    summary: str
    reasons: tuple[str, ...]
    warning: str | None = None


def build_explanation(
    *,
    direction: TrendDirection,
    confidence: ConfidenceResult,
    state: MarketState,
    ema20: float,
    ema50: float,
    rsi: float,
    ema20_previous: float,
) -> MarketExplanation:
    """
    Transforma o resultado técnico da análise em uma
    explicação legível.

    Esta camada não altera a classificação do mercado.
    Ela apenas explica os resultados produzidos pelas
    camadas anteriores.
    """

    reasons = _build_reasons(
        direction=direction,
        confidence=confidence,
        ema20=ema20,
        ema50=ema50,
        rsi=rsi,
        ema20_previous=ema20_previous,
    )

    return MarketExplanation(
        title=_build_title(state),
        summary=_build_summary(
            direction=direction,
            state=state,
            confidence=confidence,
        ),
        reasons=tuple(reasons),
        warning=_build_warning(
            direction=direction,
            state=state,
            rsi=rsi,
            confidence=confidence,
        ),
    )


def _build_title(state: MarketState) -> str:
    titles = {
        MarketState.STRONG_UPTREND:
            "Mercado em forte tendência de alta",
        MarketState.WEAK_UPTREND:
            "Mercado em tendência de alta enfraquecida",
        MarketState.NEUTRAL:
            "Mercado sem direção estrutural clara",
        MarketState.WEAK_DOWNTREND:
            "Mercado em tendência de baixa enfraquecida",
        MarketState.STRONG_DOWNTREND:
            "Mercado em forte tendência de baixa",
    }

    return titles[state]


def _build_summary(
    *,
    direction: TrendDirection,
    state: MarketState,
    confidence: ConfidenceResult,
) -> str:
    if state == MarketState.NEUTRAL:
        return (
            "As médias permanecem próximas, sem distância "
            "suficiente para confirmar uma tendência estrutural."
        )

    direction_text = (
        "compradora"
        if direction == TrendDirection.UP
        else "vendedora"
    )

    strength_text = (
        "forte"
        if confidence.score >= 75
        else "moderada"
    )

    return (
        f"A estrutura atual favorece a pressão {direction_text}, "
        f"com confiança {strength_text} de "
        f"{confidence.score:.2f}%."
    )


def _build_reasons(
    *,
    direction: TrendDirection,
    confidence: ConfidenceResult,
    ema20: float,
    ema50: float,
    rsi: float,
    ema20_previous: float,
) -> list[str]:
    reasons: list[str] = []

    reasons.append(
        _build_ema_alignment_reason(
            direction=direction,
            ema20=ema20,
            ema50=ema50,
            score=confidence.ema_distance_score,
        )
    )

    reasons.append(
        _build_rsi_reason(
            direction=direction,
            rsi=rsi,
            score=confidence.rsi_score,
        )
    )

    reasons.append(
        _build_slope_reason(
            direction=direction,
            ema20=ema20,
            ema20_previous=ema20_previous,
            score=confidence.slope_score,
        )
    )

    return reasons


def _build_ema_alignment_reason(
    *,
    direction: TrendDirection,
    ema20: float,
    ema50: float,
    score: float,
) -> str:
    if direction == TrendDirection.SIDEWAYS:
        return (
            "A EMA20 e a EMA50 permanecem próximas, "
            "sem separação estrutural relevante."
        )

    relation = (
        "acima"
        if direction == TrendDirection.UP
        else "abaixo"
    )

    if score >= 40:
        strength = "ampla"
    elif score >= 20:
        strength = "moderada"
    else:
        strength = "pequena"

    return (
        f"A EMA20 está {relation} da EMA50, com separação "
        f"{strength} entre as médias."
    )


def _build_rsi_reason(
    *,
    direction: TrendDirection,
    rsi: float,
    score: float,
) -> str:
    if direction == TrendDirection.SIDEWAYS:
        return (
            f"O RSI está em {rsi:.2f}, sem confirmação "
            "direcional relevante."
        )

    if score >= 35:
        confirmation = "forte"
    elif score >= 18:
        confirmation = "moderada"
    elif score > 0:
        confirmation = "fraca"
    else:
        confirmation = "ausente"

    side = (
        "compradora"
        if direction == TrendDirection.UP
        else "vendedora"
    )

    return (
        f"O RSI está em {rsi:.2f} e oferece confirmação "
        f"{confirmation} da pressão {side}."
    )


def _build_slope_reason(
    *,
    direction: TrendDirection,
    ema20: float,
    ema20_previous: float,
    score: float,
) -> str:
    if direction == TrendDirection.SIDEWAYS:
        return (
            "A inclinação da EMA20 não é utilizada para "
            "reforçar uma tendência lateral."
        )

    movement = ema20 - ema20_previous

    if score >= 15:
        intensity = "forte"
    elif score >= 8:
        intensity = "moderada"
    elif score > 0:
        intensity = "leve"
    else:
        intensity = "contrária"

    if direction == TrendDirection.UP:
        movement_text = (
            "positiva"
            if movement > 0
            else "negativa"
        )
    else:
        movement_text = (
            "negativa"
            if movement < 0
            else "positiva"
        )

    return (
        f"A EMA20 apresenta inclinação {movement_text}, com "
        f"confirmação {intensity} da direção analisada."
    )


def _build_warning(
    *,
    direction: TrendDirection,
    state: MarketState,
    rsi: float,
    confidence: ConfidenceResult,
) -> str | None:
    if state == MarketState.NEUTRAL:
        return (
            "O mercado está sem direção clara. Movimentos curtos "
            "podem gerar falsos sinais."
        )

    if direction == TrendDirection.UP and rsi >= 70:
        return (
            "O RSI está em região elevada. A tendência permanece "
            "compradora, mas pode ocorrer perda de aceleração ou "
            "correção."
        )

    if direction == TrendDirection.DOWN and rsi <= 30:
        return (
            "O RSI está em região baixa. A tendência permanece "
            "vendedora, mas pode ocorrer perda de aceleração ou "
            "repique."
        )

    if confidence.slope_score < 8:
        return (
            "A estrutura direcional permanece válida, mas a "
            "inclinação da EMA20 indica baixa aceleração."
        )

    return None