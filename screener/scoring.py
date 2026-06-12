import pandas as pd

from infrastructure.logger import logger

# ======================================
# AI SCORING SYSTEM
# ======================================


def calculate_score(row):

    try:

        # ======================================
        # REQUIRED COLUMNS
        # ======================================

        required_columns = [
            "Close",
            "MA5",
            "MA20",
            "MA50",
            "EMA20",
            "EMA50",
            "RSI",
            "MACD",
            "MACD_SIGNAL",
            "MACD_HIST",
            "Volume",
            "VOL_MA20",
            "BB_MIDDLE",
            "BB_UPPER",
            "BB_WIDTH",
            "HIGH_20",
            "ADX",
            "WEEKLY_RETURN",
            "MONTHLY_RETURN",
            "VOLATILITY",
            "ATR",
            "DISTANCE_MA20",
        ]

        # ======================================
        # VALIDATION
        # ======================================

        for column in required_columns:

            if column not in row:

                return {"score": 0, "confidence": "INVALID"}

            if pd.isna(row[column]):

                return {"score": 0, "confidence": "INVALID"}

        # ======================================
        # SCORE CONTAINERS
        # ======================================

        trend_score = 0

        momentum_score = 0

        volume_score = 0

        volatility_score = 0

        breakout_score = 0

        risk_penalty = 0

        # ======================================
        # TREND STRUCTURE
        # ======================================

        if row["Close"] > row["MA5"]:

            trend_score += 5

        if row["Close"] > row["MA20"]:

            trend_score += 10

        if row["Close"] > row["MA50"]:

            trend_score += 10

        if row["Close"] > row["EMA20"]:

            trend_score += 10

        if row["EMA20"] > row["EMA50"]:

            trend_score += 15

        if row["MA5"] > row["MA20"]:

            trend_score += 10

        # ======================================
        # RSI MOMENTUM
        # ======================================

        if row["RSI"] >= 50:

            momentum_score += 5

        if row["RSI"] >= 60:

            momentum_score += 10

        if 65 <= row["RSI"] <= 75:

            momentum_score += 10

        if row["RSI"] >= 80:

            risk_penalty += 15

        if row["RSI"] < 45:

            risk_penalty += 10

        # ======================================
        # MACD MOMENTUM
        # ======================================

        if row["MACD"] > row["MACD_SIGNAL"]:

            momentum_score += 10

        if row["MACD_HIST"] > 0:

            momentum_score += 5

        # ======================================
        # VOLUME ANALYSIS
        # ======================================

        if row["VOL_MA20"] > 0:

            volume_ratio = row["Volume"] / row["VOL_MA20"]

        else:

            volume_ratio = 0

        if volume_ratio > 1:

            volume_score += 10

        if volume_ratio > 1.5:

            volume_score += 15

        if volume_ratio > 2.5:

            volume_score += 5

        # ======================================
        # BOLLINGER ANALYSIS
        # ======================================

        if row["Close"] > row["BB_MIDDLE"]:

            trend_score += 5

        if row["Close"] > row["BB_UPPER"]:

            breakout_score += 10

        bb_width_ratio = row["BB_WIDTH"] / row["Close"]

        if bb_width_ratio > 0.05:

            breakout_score += 5

        # ======================================
        # BREAKOUT DETECTION
        # ======================================

        if row["Close"] >= row["HIGH_20"]:

            breakout_score += 20

        # ======================================
        # ADX TREND STRENGTH
        # ======================================

        if row["ADX"] >= 20:

            trend_score += 5

        if row["ADX"] >= 25:

            trend_score += 10

        if row["ADX"] >= 35:

            trend_score += 5

        # ======================================
        # MOMENTUM FILTER
        # ======================================

        weekly_return = row["WEEKLY_RETURN"]

        monthly_return = row["MONTHLY_RETURN"]

        if 0.05 <= weekly_return <= 0.30:

            momentum_score += 10

        if monthly_return > 0:

            momentum_score += 5

        if weekly_return > 0.30:

            risk_penalty += 10

        # ======================================
        # VOLATILITY FILTER
        # ======================================

        volatility = row["VOLATILITY"]

        if volatility < 0.05:

            volatility_score += 5

        if volatility > 0.12:

            risk_penalty += 10

        # ======================================
        # ATR FILTER
        # ======================================

        atr_percent = row["ATR"] / row["Close"]

        if 0.02 <= atr_percent <= 0.08:

            volatility_score += 5

        if atr_percent > 0.10:

            risk_penalty += 10

        # ======================================
        # DISTANCE FROM MA20
        # ======================================

        distance_ma20 = abs(row["DISTANCE_MA20"])

        if distance_ma20 <= 15:

            trend_score += 5

        if distance_ma20 > 25:

            risk_penalty += 10

        # ======================================
        # FINAL SCORE
        # ======================================

        raw_score = (
            trend_score
            + momentum_score
            + volume_score
            + volatility_score
            + breakout_score
            - risk_penalty
        )

        # ======================================
        # NORMALIZATION
        # ======================================

        score = max(0, min(100, raw_score))

        # ======================================
        # CONFIDENCE
        # ======================================

        confidence = "LOW"

        if score >= 85:

            confidence = "ELITE"

        elif score >= 70:

            confidence = "HIGH"

        elif score >= 55:

            confidence = "MEDIUM"

        # ======================================
        # RESULT
        # ======================================

        return {
            "score": int(score),
            "confidence": confidence,
            "trend_score": (trend_score),
            "momentum_score": (momentum_score),
            "volume_score": (volume_score),
            "volatility_score": (volatility_score),
            "breakout_score": (breakout_score),
            "risk_penalty": (risk_penalty),
        }

    except Exception as e:

        logger.error(f"Scoring Error: {e}")

        return {"score": 0, "confidence": "ERROR"}
