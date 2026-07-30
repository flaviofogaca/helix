from dataclasses import dataclass
from datetime import datetime

import MetaTrader5 as mt5
import pandas as pd


DEFAULT_CANDLE_COUNT = 500


@dataclass(frozen=True)
class MarketIndicators:
    symbol: str
    timeframe: str
    candle_time: datetime
    close: float
    ema20: float
    ema50: float
    ema20_previous: float
    rsi: float


def connect_mt5() -> None:
    """
    Inicializa a conexão entre o Python e o terminal MetaTrader 5.

    O MT5 deve estar aberto e autenticado em uma conta.
    """

    if mt5.initialize():
        return

    error_code, error_message = mt5.last_error()

    raise ConnectionError(
        "Não foi possível conectar ao MetaTrader 5. "
        f"Erro {error_code}: {error_message}"
    )


def disconnect_mt5() -> None:
    """
    Encerra a conexão com o terminal MetaTrader 5.
    """

    mt5.shutdown()


def get_market_indicators(
    symbol: str,
    timeframe: int = mt5.TIMEFRAME_M5,
    candle_count: int = DEFAULT_CANDLE_COUNT,
) -> MarketIndicators:
    """
    Busca candles no MT5 e calcula os indicadores usados pelo Helix.

    A análise usa o último candle fechado, ignorando o candle atual
    que ainda pode estar em formação.
    """

    if candle_count < 100:
        raise ValueError(
            "candle_count deve ser pelo menos 100 para estabilizar "
            "o cálculo dos indicadores."
        )

    _ensure_symbol_available(symbol)

    rates = mt5.copy_rates_from_pos(
        symbol,
        timeframe,
        0,
        candle_count,
    )

    if rates is None:
        error_code, error_message = mt5.last_error()

        raise RuntimeError(
            f"Não foi possível buscar candles de {symbol}. "
            f"Erro {error_code}: {error_message}"
        )

    if len(rates) < 52:
        raise RuntimeError(
            f"Foram recebidos apenas {len(rates)} candles de {symbol}. "
            "São necessários pelo menos 52."
        )

    dataframe = pd.DataFrame(rates)

    dataframe["time"] = pd.to_datetime(
        dataframe["time"],
        unit="s",
        utc=True,
    )

    dataframe["ema20"] = (
        dataframe["close"]
        .ewm(span=20, adjust=False)
        .mean()
    )

    dataframe["ema50"] = (
        dataframe["close"]
        .ewm(span=50, adjust=False)
        .mean()
    )

    dataframe["rsi"] = _calculate_rsi(
        close=dataframe["close"],
        period=14,
    )

    # -1: candle atual, ainda em formação.
    # -2: último candle completamente fechado.
    # -3: candle anterior ao último fechado.
    last_closed = dataframe.iloc[-2]
    previous_closed = dataframe.iloc[-3]

    required_values = [
        last_closed["close"],
        last_closed["ema20"],
        last_closed["ema50"],
        last_closed["rsi"],
        previous_closed["ema20"],
    ]

    if any(pd.isna(value) for value in required_values):
        raise RuntimeError(
            "Os indicadores ainda possuem valores inválidos. "
            "Tente aumentar a quantidade de candles."
        )

    return MarketIndicators(
        symbol=symbol,
        timeframe=_timeframe_to_string(timeframe),
        candle_time=last_closed["time"].to_pydatetime(),
        close=float(last_closed["close"]),
        ema20=float(last_closed["ema20"]),
        ema50=float(last_closed["ema50"]),
        ema20_previous=float(previous_closed["ema20"]),
        rsi=float(last_closed["rsi"]),
    )


def _ensure_symbol_available(symbol: str) -> None:
    """
    Confirma que o ativo existe e está habilitado no Market Watch.
    """

    symbol_info = mt5.symbol_info(symbol)

    if symbol_info is None:
        raise ValueError(
            f"O ativo '{symbol}' não foi encontrado no MT5."
        )

    if symbol_info.visible:
        return

    if not mt5.symbol_select(symbol, True):
        error_code, error_message = mt5.last_error()

        raise RuntimeError(
            f"Não foi possível habilitar '{symbol}' no Market Watch. "
            f"Erro {error_code}: {error_message}"
        )


def _calculate_rsi(
    close: pd.Series,
    period: int,
) -> pd.Series:
    """
    Calcula o RSI usando a suavização de Wilder.
    """

    price_change = close.diff()

    gains = price_change.clip(lower=0.0)
    losses = -price_change.clip(upper=0.0)

    average_gain = gains.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period,
    ).mean()

    average_loss = losses.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period,
    ).mean()

    relative_strength = average_gain / average_loss

    rsi = 100 - (
        100 / (1 + relative_strength)
    )

    # Mercado sem perdas no período equivale a RSI 100.
    rsi = rsi.mask(
        (average_loss == 0) & (average_gain > 0),
        100.0,
    )

    # Mercado completamente parado equivale a RSI neutro.
    rsi = rsi.mask(
        (average_loss == 0) & (average_gain == 0),
        50.0,
    )

    return rsi


def _timeframe_to_string(timeframe: int) -> str:
    """
    Converte os timeframes utilizados inicialmente pelo Helix
    para uma representação legível.
    """

    timeframe_names = {
        mt5.TIMEFRAME_M1: "M1",
        mt5.TIMEFRAME_M5: "M5",
        mt5.TIMEFRAME_M15: "M15",
        mt5.TIMEFRAME_M30: "M30",
        mt5.TIMEFRAME_H1: "H1",
    }

    return timeframe_names.get(
        timeframe,
        str(timeframe),
    )