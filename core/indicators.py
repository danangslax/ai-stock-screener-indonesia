import ta

def add_indicators(df):

    # =========================
    # MOVING AVERAGE
    # =========================

    df["MA5"] = ta.trend.sma_indicator(
        df["Close"],
        window=5
    )

    df["MA20"] = ta.trend.sma_indicator(
        df["Close"],
        window=20
    )

    # =========================
    # VOLUME MA20
    # =========================

    df["VOL_MA20"] = ta.trend.sma_indicator(
        df["Volume"],
        window=20
    )

    # =========================
    # RSI
    # =========================

    df["RSI"] = ta.momentum.rsi(
        df["Close"],
        window=14
    )

    # =========================
    # BOLLINGER BAND
    # =========================

    bb = ta.volatility.BollingerBands(
        close=df["Close"],
        window=20,
        window_dev=2
    )

    df["BB_UPPER"] = bb.bollinger_hband()

    df["BB_MIDDLE"] = bb.bollinger_mavg()

    df["BB_LOWER"] = bb.bollinger_lband()

    return df