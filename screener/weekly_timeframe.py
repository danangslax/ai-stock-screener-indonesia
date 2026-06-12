import pandas as pd

from infrastructure.logger import logger

# ======================================
# WEEKLY TIMEFRAME ANALYSIS
# ======================================


def analyze_weekly_timeframe(df):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if df.empty:

            return None

        if len(df) < 200:

            return None

        # ======================================
        # RESAMPLE TO WEEKLY
        # ======================================

        weekly_df = df.resample("W").agg(
            {
                "Open": "first",
                "High": "max",
                "Low": "min",
                "Close": "last",
                "Volume": "sum",
                "EMA20": "last",
                "EMA50": "last",
                "EMA200": "last",
                "RSI": "last",
                "ADX": "last",
                "VOLATILITY": "last",
                "ATR": "last",
                "VOL_MA20": "last",
            }
        )

        weekly_df = weekly_df.dropna()

        # ======================================
        # VALIDATION
        # ======================================

        if weekly_df.empty:

            return None

        if len(weekly_df) < 20:

            return None

        latest = weekly_df.iloc[-1]

        previous = weekly_df.iloc[-2]

        # ======================================
        # REQUIRED COLUMNS
        # ======================================

        required_columns = [
            "Close",
            "EMA20",
            "EMA50",
            "EMA200",
            "RSI",
            "ADX",
            "VOLATILITY",
            "ATR",
            "Volume",
            "VOL_MA20",
        ]

        for col in required_columns:

            if col not in latest:

                return None

            if pd.isna(latest[col]):

                return None

        # ======================================
        # BASIC DATA
        # ======================================

        close = float(latest["Close"])

        ema20 = float(latest["EMA20"])

        ema50 = float(latest["EMA50"])

        ema200 = float(latest["EMA200"])

        rsi = float(latest["RSI"])

        adx = float(latest["ADX"])

        volatility = float(latest["VOLATILITY"])

        atr = float(latest["ATR"])

        volume = float(latest["Volume"])

        vol_ma20 = float(latest["VOL_MA20"])

        # ======================================
        # VALIDATION
        # ======================================

        if vol_ma20 <= 0:

            return None

        # ======================================
        # METRICS
        # ======================================

        volume_ratio = round(volume / vol_ma20, 2)

        atr_percent = round(atr / close, 4)

        # ======================================
        # SCORE CONTAINERS
        # ======================================

        trend_score = 0

        momentum_score = 0

        stability_score = 0

        # ======================================
        # TREND STRUCTURE
        # ======================================

        if close > ema20:

            trend_score += 10

        if ema20 > ema50:

            trend_score += 20

        if ema50 > ema200:

            trend_score += 25

        if close > ema20 and ema20 > ema50 and ema50 > ema200:

            trend_score += 15

        # ======================================
        # MOMENTUM
        # ======================================

        if rsi >= 50:

            momentum_score += 10

        if rsi >= 65:

            momentum_score += 5

        if adx >= 20:

            momentum_score += 10

        if adx >= 35:

            momentum_score += 5

        # ======================================
        # VOLUME CONFIRMATION
        # ======================================

        if volume_ratio > 1:

            momentum_score += 5

        # ======================================
        # STABILITY
        # ======================================

        if volatility < 0.08:

            stability_score += 5

        if 0.02 <= atr_percent <= 0.10:

            stability_score += 5

        # ======================================
        # FINAL SCORE
        # ======================================

        score = trend_score + momentum_score + stability_score

        score = min(score, 100)

        # ======================================
        # STATUS
        # ======================================

        if score >= 80:

            status = "STRONG"

        elif score >= 65:

            status = "GOOD"

        else:

            status = "WEAK"

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
            "status": status,
            "score": score,
            "confidence": confidence,
            "close": round(close, 2),
            "ema20": round(ema20, 2),
            "ema50": round(ema50, 2),
            "ema200": round(ema200, 2),
            "rsi": round(rsi, 2),
            "adx": round(adx, 2),
            "volume_ratio": (volume_ratio),
            "atr_percent": (atr_percent),
        }

    except Exception as e:

        logger.error(f"Weekly analysis " f"error: {e}")

        return None
