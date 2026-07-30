import MetaTrader5 as mt5

from src.analysis.engine import analyze_market
from src.market_data import (
    connect_mt5,
    disconnect_mt5,
    get_market_indicators,
)


SYMBOL = "WINQ26"
TIMEFRAME = mt5.TIMEFRAME_M5


def main() -> None:
    try:
        connect_mt5()

        indicators = get_market_indicators(
            symbol=SYMBOL,
            timeframe=TIMEFRAME,
            candle_count=500,
        )

        result = analyze_market(
            ema20=indicators.ema20,
            ema50=indicators.ema50,
            rsi=indicators.rsi,
            ema20_previous=indicators.ema20_previous,
        )

        print()
        print("================ HELIX LIVE ANALYSIS ================")
        print(f"Ativo: {indicators.symbol}")
        print(f"Timeframe: {indicators.timeframe}")
        print(
            "Candle analisado: "
            f"{indicators.candle_time:%d/%m/%Y %H:%M:%S %Z}"
        )
        print(f"Fechamento: {indicators.close:.2f}")
        print(f"EMA20: {indicators.ema20:.2f}")
        print(f"EMA50: {indicators.ema50:.2f}")
        print(f"EMA20 anterior: {indicators.ema20_previous:.2f}")
        print(f"RSI: {indicators.rsi:.2f}")
        print("-----------------------------------------------------")
        print(f"Direção: {result.direction.value}")
        print(f"Confiança: {result.confidence.score:.2f}%")
        print(
            "Distância das EMAs: "
            f"{result.confidence.ema_distance_score:.2f}"
        )
        print(
            "Confirmação do RSI: "
            f"{result.confidence.rsi_score:.2f}"
        )
        print(
            "Inclinação da EMA20: "
            f"{result.confidence.slope_score:.2f}"
        )
        print(f"Estado: {result.state.value}")
        print("=====================================================")
        print()

        print()
        print("================ HELIX EXPLANATION =================")
        print(result.explanation.title)
        print(result.explanation.summary)
        print()

        for reason in result.explanation.reasons:
            print(f"- {reason}")

        if result.explanation.warning:
            print()
            print(f"Atenção: {result.explanation.warning}")

        print("====================================================")

    except Exception as error:
        print()
        print("================ HELIX ERROR =================")
        print(error)
        print("==============================================")
        print()

    finally:
        disconnect_mt5()


if __name__ == "__main__":
    main()