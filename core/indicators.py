import ta

# ======================================
# ADD TECHNICAL INDICATORS
# ======================================

def add_indicators(df):

    # ======================================
    # VALIDATION
    # ======================================

    if df.empty:

        return df

    # ======================================
    # MOVING AVERAGE
    # ======================================

    df["MA5"] = ta.trend.sma_indicator(

        df["Close"],

        window=5
    )

    df["MA20"] = ta.trend.sma_indicator(

        df["Close"],

        window=20
    )

    # ======================================
    # EMA
    # ======================================

    df["EMA20"] = ta.trend.ema_indicator(

        df["Close"],

        window=20
    )

    df["EMA50"] = ta.trend.ema_indicator(

        df["Close"],

        window=50
    )

    df["EMA200"] = ta.trend.ema_indicator(

        df["Close"],

        window=200
    )

    # ======================================
    # VOLUME MA
    # ======================================

    df["VOL_MA20"] = ta.trend.sma_indicator(

        df["Volume"],

        window=20
    )

    # ======================================
    # RSI
    # ======================================

    df["RSI"] = ta.momentum.rsi(

        df["Close"],

        window=14
    )

    # ======================================
    # ATR
    # ======================================

    df["ATR"] = ta.volatility.average_true_range(

        high=df["High"],

        low=df["Low"],

        close=df["Close"],

        window=14
    )

    # ======================================
    # ADX
    # ======================================

    df["ADX"] = ta.trend.adx(

        high=df["High"],

        low=df["Low"],

        close=df["Close"],

        window=14
    )

    # ======================================
    # BOLLINGER BANDS
    # ======================================

    bb = ta.volatility.BollingerBands(

        close=df["Close"],

        window=20,

        window_dev=2
    )

    df["BB_UPPER"] = (
        bb.bollinger_hband()
    )

    df["BB_MIDDLE"] = (
        bb.bollinger_mavg()
    )

    df["BB_LOWER"] = (
        bb.bollinger_lband()
    )

    # ======================================
    # VOLATILITY
    # ======================================

    df["VOLATILITY"] = (

        df["Close"]
        .pct_change()
        .rolling(20)
        .std()
    )

    # ======================================
    # MACD
    # ======================================

    macd = ta.trend.MACD(

        close=df["Close"]
    )

    df["MACD"] = (
        macd.macd()
    )

    df["MACD_SIGNAL"] = (
        macd.macd_signal()
    )

    df["MACD_HIST"] = (
        macd.macd_diff()
    )

    # ======================================
    # CLEAN DATA
    # ======================================

    df = df.dropna()

    return df