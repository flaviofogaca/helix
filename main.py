import MetaTrader5 as mt5

from src.filters.session import filter_market_session
from src.analysis.trend import analyze_trend
from src.market_data import connect_mt5, shutdown_mt5, get_candles
from src.indicators.engine import calculate_indicators


def main():
    symbol = "WIN$"
    timeframe = mt5.TIMEFRAME_M5

    try:
        connect_mt5()

        df = get_candles(symbol, timeframe, 500)
        df = filter_market_session(df, start="09:00", end="18:00")
        df = calculate_indicators(df)

        analysis = analyze_trend(df)

        ema20 = df["EMA20"].iloc[-1]
        ema50 = df["EMA50"].iloc[-1]
        rsi = df["RSI"].iloc[-1]
        ultimo_preco = df["close"].iloc[-1]

        print("\n==============================")
        print("        HELIX V0.1")
        print("==============================")
        print(f"Ativo............. {symbol}")
        print(f"Último preço...... {ultimo_preco:.2f}")
        print(f"EMA20............. {ema20:.2f}")
        print(f"EMA50............. {ema50:.2f}")
        print(f"RSI............... {rsi:.2f}")
        print(f"Tendência......... {analysis['emoji']} {analysis['trend']}")
        print(f"Score............. {analysis['score']}/{analysis['max_score']}")
        print()
        print("Evidências")
        
        for reason in analysis["reasons"]:
            print(f"✔ {reason}")
        print("==============================")

        print(df[["time", "close", "RSI"]].tail(10))

    finally:
        shutdown_mt5()


if __name__ == "__main__":
    main()