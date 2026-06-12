import ta

import pandas as pd

from infrastructure.logger import logger

# ======================================
# REQUIRED COLUMNS
# ======================================

REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]

# ======================================
# ADD TECHNICAL INDICATORS
# ======================================


def add_indicators(df):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if df.empty:

            logger.warning("Empty dataframe")

            return pd.DataFrame()

        # ======================================
        # COPY DATAFRAME
        # ======================================

        df = df.copy()

        # ======================================
        # REQUIRED COLUMNS
        # ======================================

        for column in REQUIRED_COLUMNS:

            if column not in df.columns:

                raise ValueError(f"Missing column: {column}")

        # ======================================
        # MINIMUM DATA
        # ======================================

        if len(df) < 200:

            logger.warning("Insufficient data " "for EMA200")

            return pd.DataFrame()

        # ======================================
        # FORCE NUMERIC
        # ======================================

        df[REQUIRED_COLUMNS] = df[REQUIRED_COLUMNS].astype(float)

        # ======================================
        # SIMPLE MOVING AVERAGE
        # ======================================

        df["MA5"] = ta.trend.sma_indicator(close=df["Close"], window=5)

        df["MA20"] = ta.trend.sma_indicator(close=df["Close"], window=20)

        df["MA50"] = ta.trend.sma_indicator(close=df["Close"], window=50)

        # ======================================
        # EXPONENTIAL MOVING AVERAGE
        # ======================================

        df["EMA20"] = ta.trend.ema_indicator(close=df["Close"], window=20)

        df["EMA50"] = ta.trend.ema_indicator(close=df["Close"], window=50)

        df["EMA200"] = ta.trend.ema_indicator(close=df["Close"], window=200)

        # ======================================
        # VOLUME MOVING AVERAGE
        # ======================================

        df["VOL_MA20"] = df["Volume"].rolling(20).mean()

        # ======================================
        # RSI
        # ======================================

        df["RSI"] = ta.momentum.rsi(close=df["Close"], window=14)

        # ======================================
        # MACD
        # ======================================

        macd = ta.trend.MACD(close=df["Close"])

        df["MACD"] = macd.macd()

        df["MACD_SIGNAL"] = macd.macd_signal()

        df["MACD_HIST"] = macd.macd_diff()

        # ======================================
        # ATR
        # ======================================

        df["ATR"] = ta.volatility.average_true_range(
            high=df["High"], low=df["Low"], close=df["Close"], window=14
        )

        # ======================================
        # ADX
        # ======================================

        df["ADX"] = ta.trend.adx(
            high=df["High"], low=df["Low"], close=df["Close"], window=14
        )

        # ======================================
        # BOLLINGER BANDS
        # ======================================

        bb = ta.volatility.BollingerBands(close=df["Close"], window=20, window_dev=2)

        df["BB_UPPER"] = bb.bollinger_hband()

        df["BB_MIDDLE"] = bb.bollinger_mavg()

        df["BB_LOWER"] = bb.bollinger_lband()

        df["BB_WIDTH"] = df["BB_UPPER"] - df["BB_LOWER"]

        # ======================================
        # BREAKOUT LEVELS
        # ======================================

        df["HIGH_20"] = df["High"].rolling(20).max()

        df["LOW_20"] = df["Low"].rolling(20).min()

        # ======================================
        # MOMENTUM
        # ======================================

        df["WEEKLY_RETURN"] = df["Close"].pct_change(5)

        df["MONTHLY_RETURN"] = df["Close"].pct_change(20)

        # ======================================
        # VOLATILITY
        # ======================================

        df["VOLATILITY"] = df["Close"].pct_change().rolling(20).std()

        # ======================================
        # PRICE DISTANCE
        # ======================================

        df["DISTANCE_MA20"] = ((df["Close"] - df["MA20"]) / df["MA20"]) * 100

        # ======================================
        # CLEAN DATA
        # ======================================

        df = df.dropna()

        df = df.sort_index()

        logger.info("Indicators added")

        return df

    except Exception as e:

        logger.error(f"Indicator Error: {e}")

        return pd.DataFrame()
