import ta
import pandas as pd

# ======================================
# ADD TECHNICAL INDICATORS
# ======================================

def add_indicators(df):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if df.empty:

            return df

        required_columns = [

            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]

        for column in required_columns:

            if column not in df.columns:

                raise ValueError(
                    f"Missing column: {column}"
                )

        # ======================================
        # SIMPLE MOVING AVERAGE
        # ======================================

        df["MA5"] = ta.trend.sma_indicator(
            close=df["Close"],
            window=5
        )

        df["MA20"] = ta.trend.sma_indicator(
            close=df["Close"],
            window=20
        )

        df["MA50"] = ta.trend.sma_indicator(
            close=df["Close"],
            window=50
        )

        # ======================================
        # EXPONENTIAL MOVING AVERAGE
        # ======================================

        df["EMA20"] = ta.trend.ema_indicator(
            close=df["Close"],
            window=20
        )

        df["EMA50"] = ta.trend.ema_indicator(
            close=df["Close"],
            window=50
        )

        # ======================================
        # VOLUME MOVING AVERAGE
        # ======================================

        df["VOL_MA20"] = ta.trend.sma_indicator(
            close=df["Volume"],
            window=20
        )

        # ======================================
        # RSI
        # ======================================

        df["RSI"] = ta.momentum.rsi(
            close=df["Close"],
            window=14
        )

        # ======================================
        # MACD
        # ======================================

        macd = ta.trend.MACD(
            close=df["Close"]
        )

        df["MACD"] = macd.macd()

        df["MACD_SIGNAL"] = (
            macd.macd_signal()
        )

        df["MACD_HIST"] = (
            macd.macd_diff()
        )

        # ======================================
        # ATR
        # ======================================

        df["ATR"] = (
            ta.volatility.average_true_range(
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                window=14
            )
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

        df["BB_WIDTH"] = (
            df["BB_UPPER"]
            - df["BB_LOWER"]
        )

        # ======================================
        # BREAKOUT LEVELS
        # ======================================

        df["HIGH_20"] = (
            df["High"]
            .rolling(20)
            .max()
        )

        df["LOW_20"] = (
            df["Low"]
            .rolling(20)
            .min()
        )

        # ======================================
        # MOMENTUM
        # ======================================

        df["WEEKLY_RETURN"] = (
            df["Close"].pct_change(5)
        )

        df["MONTHLY_RETURN"] = (
            df["Close"].pct_change(20)
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
        # PRICE DISTANCE
        # ======================================

        df["DISTANCE_MA20"] = (
            (
                df["Close"]
                - df["MA20"]
            )
            / df["MA20"]
        ) * 100

        # ======================================
        # CLEAN DATA
        # ======================================

        df = df.copy()

        df = df.dropna()

        df = df.sort_index()

        print(
            "✅ Indicators added"
        )

        return df

    except Exception as e:

        print(
            f"❌ Indicator Error: {e}"
        )

        return pd.DataFrame()
    
# ======================================
# EMA 200
# ======================================

df["EMA200"] = ta.trend.ema_indicator(

    df["Close"],

    window=200
)

# ======================================
# MACD
# ======================================

macd = ta.trend.MACD(

    close=df["Close"]
)

df["MACD"] = macd.macd()

df["MACD_SIGNAL"] = (
    macd.macd_signal()
)

df["MACD_HIST"] = (
    macd.macd_diff()
)