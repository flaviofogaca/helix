from dataclasses import dataclass

from src.analysis.trend import TrendDirection


EMA_DISTANCE_MAX_SCORE = 45.0
RSI_MAX_SCORE = 35.0
SLOPE_MAX_SCORE = 20.0

EMA_DISTANCE_FULL_STRENGTH = 0.002
EMA_SLOPE_FULL_STRENGTH = 0.0005


@dataclass(frozen=True)
class ConfidenceResult:
    """
    Resultado detalhado do cálculo de confiança.

    O score total varia de 0 a 100 e é composto pelas
    contribuições da distância entre médias, RSI e inclinação.
    """

    score: float
    ema_distance_score: float
    rsi_score: float
    slope_score: float


def calculate_confidence(
    direction: TrendDirection,
    ema20: float,
    ema50: float,
    rsi: float,
    ema20_previous: float,
) -> ConfidenceResult:
    """
    Calcula a confiança da direção identificada pelo Helix.

    Pesos:
    - Distância entre EMA20 e EMA50: 45 pontos
    - Confirmação pelo RSI: 35 pontos
    - Inclinação da EMA20: 20 pontos

    Args:
        direction:
            Direção estrutural previamente identificada.

        ema20:
            Valor atual da EMA20.

        ema50:
            Valor atual da EMA50.

        rsi:
            Valor atual do RSI, entre 0 e 100.

        ema20_previous:
            Valor da EMA20 no candle anterior.

    Returns:
        ConfidenceResult com score total e contribuições individuais.

    Raises:
        TypeError:
            Caso direction não seja uma instância de TrendDirection.

        ValueError:
            Caso algum valor recebido seja inválido.
    """

    _validate_inputs(
        direction=direction,
        ema20=ema20,
        ema50=ema50,
        rsi=rsi,
        ema20_previous=ema20_previous,
    )

    if direction == TrendDirection.SIDEWAYS:
        return ConfidenceResult(
            score=0.0,
            ema_distance_score=0.0,
            rsi_score=0.0,
            slope_score=0.0,
        )

    ema_distance_score = _calculate_ema_distance_score(
        ema20=ema20,
        ema50=ema50,
    )

    rsi_score = _calculate_rsi_score(
        direction=direction,
        rsi=rsi,
    )

    slope_score = _calculate_slope_score(
        direction=direction,
        ema20=ema20,
        ema20_previous=ema20_previous,
    )

    total_score = (
        ema_distance_score
        + rsi_score
        + slope_score
    )

    return ConfidenceResult(
        score=_round_score(min(total_score, 100.0)),
        ema_distance_score=_round_score(ema_distance_score),
        rsi_score=_round_score(rsi_score),
        slope_score=_round_score(slope_score),
    )


def _validate_inputs(
    direction: TrendDirection,
    ema20: float,
    ema50: float,
    rsi: float,
    ema20_previous: float,
) -> None:
    """
    Valida os dados necessários para o cálculo de confiança.
    """

    if not isinstance(direction, TrendDirection):
        raise TypeError(
            "direction deve ser uma instância de TrendDirection."
        )

    if ema20 <= 0:
        raise ValueError("EMA20 deve ser maior que zero.")

    if ema50 <= 0:
        raise ValueError("EMA50 deve ser maior que zero.")

    if ema20_previous <= 0:
        raise ValueError("EMA20 anterior deve ser maior que zero.")

    if not 0 <= rsi <= 100:
        raise ValueError("RSI deve estar entre 0 e 100.")


def _calculate_ema_distance_score(
    ema20: float,
    ema50: float,
) -> float:
    """
    Calcula a confiança estrutural usando a distância relativa
    entre a EMA20 e a EMA50.

    Uma distância de 0,20% ou mais recebe a pontuação máxima.

    Returns:
        Pontuação entre 0 e 45.
    """

    relative_distance = abs(ema20 - ema50) / ema50

    normalized_distance = min(
        relative_distance / EMA_DISTANCE_FULL_STRENGTH,
        1.0,
    )

    return normalized_distance * EMA_DISTANCE_MAX_SCORE


def _calculate_rsi_score(
    direction: TrendDirection,
    rsi: float,
) -> float:
    """
    Avalia o quanto o RSI confirma a direção identificada.

    Returns:
        Pontuação entre 0 e 35.
    """

    if direction == TrendDirection.UP:
        return _calculate_uptrend_rsi_score(rsi)

    if direction == TrendDirection.DOWN:
        return _calculate_downtrend_rsi_score(rsi)

    return 0.0


def _calculate_uptrend_rsi_score(rsi: float) -> float:
    """
    Calcula a confirmação do RSI para uma tendência de alta.
    """

    if rsi >= 60:
        return RSI_MAX_SCORE

    if rsi >= 55:
        return 28.0

    if rsi >= 50:
        return 18.0

    if rsi >= 45:
        return 8.0

    return 0.0


def _calculate_downtrend_rsi_score(rsi: float) -> float:
    """
    Calcula a confirmação do RSI para uma tendência de baixa.
    """

    if rsi <= 40:
        return RSI_MAX_SCORE

    if rsi <= 45:
        return 28.0

    if rsi <= 50:
        return 18.0

    if rsi <= 55:
        return 8.0

    return 0.0


def _calculate_slope_score(
    direction: TrendDirection,
    ema20: float,
    ema20_previous: float,
) -> float:
    """
    Verifica se a EMA20 está inclinada na mesma direção
    da tendência identificada.

    Uma inclinação relativa favorável de 0,05% ou mais
    recebe a pontuação máxima.

    Returns:
        Pontuação entre 0 e 20.
    """

    relative_slope = (
        ema20 - ema20_previous
    ) / ema20_previous

    directional_slope = _get_directional_slope(
        direction=direction,
        relative_slope=relative_slope,
    )

    if directional_slope <= 0:
        return 0.0

    normalized_slope = min(
        directional_slope / EMA_SLOPE_FULL_STRENGTH,
        1.0,
    )

    return normalized_slope * SLOPE_MAX_SCORE


def _get_directional_slope(
    direction: TrendDirection,
    relative_slope: float,
) -> float:
    """
    Converte a inclinação da EMA20 para a perspectiva
    da direção analisada.

    Valores positivos indicam que a inclinação confirma
    a tendência.
    """

    if direction == TrendDirection.UP:
        return relative_slope

    if direction == TrendDirection.DOWN:
        return -relative_slope

    return 0.0


def _round_score(value: float) -> float:
    """
    Padroniza o arredondamento dos componentes de confiança.
    """

    return round(value, 2)