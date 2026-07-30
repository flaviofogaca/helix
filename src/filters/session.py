import pandas as pd


def filter_market_session(df, start="09:00", end="18:00"):
    start_time = pd.to_datetime(start).time()
    end_time = pd.to_datetime(end).time()

    return df[
        (df["time"].dt.time >= start_time) &
        (df["time"].dt.time <= end_time)
    ].copy()