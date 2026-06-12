import pandas as pd

from infrastructure.logger import logger

# ======================================
# DAILY TIMEFRAME ANALYSIS
# ======================================


def analyze_daily_timeframe(df):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if df.empty:

            return None

        if len(df) < 200:

            return None

        latest = df.iloc[-1]

        previous = df.iloc[-2]

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
            "MACD",
            "MACD_SIGNAL",
            "Volume",
            "VOL_MA20",
            "VOLATILITY",
            "ATR",
        ]

        for col in required_columns:

            if col not in df.columns:

                return None

            if pd.isna(latest[col]):

                return None

        # ======================================
        # BASIC DATA
        # ======================================

        close_price = float(latest["Close"])

        ema20 = float(latest["EMA20"])

        ema50 = float(latest["EMA50"])

        ema200 = float(latest["EMA200"])

        rsi = float(latest["RSI"])

        adx = float(latest["ADX"])

        macd = float(latest["MACD"])

        macd_signal = float(latest["MACD_SIGNAL"])

        volume = float(latest["Volume"])

        vol_ma20 = float(latest["VOL_MA20"])

        volatility = float(latest["VOLATILITY"])

        atr = float(latest["ATR"])

        # ======================================
        # VALIDATION
        # ======================================

        if vol_ma20 <= 0:

            return None

        # ======================================
        # METRICS
        # ======================================

        volume_ratio = round(volume / vol_ma20, 2)

        atr_percent = round(atr / close_price, 4)

        # ======================================
        # SCORE CONTAINERS
        # ======================================

        trend_score = 0

        momentum_score = 0

        volume_score = 0

        stability_score = 0

        # ======================================
        # TREND STRUCTURE
        # ======================================

        if close_price > ema20:

            trend_score += 10

        if ema20 > ema50:

            trend_score += 15

        if ema50 > ema200:

            trend_score += 20

        if close_price > ema20 and ema20 > ema50 and ema50 > ema200:

            trend_score += 20

        # ======================================
        # MOMENTUM
        # ======================================

        if rsi >= 50:

            momentum_score += 10

        if rsi >= 65:

            momentum_score += 5

        if adx >= 18:

            momentum_score += 10

        if adx >= 35:

            momentum_score += 5

        # ======================================
        # MACD CONFIRMATION
        # ======================================

        if macd > macd_signal:

            momentum_score += 10

        if previous["MACD"] < previous["MACD_SIGNAL"] and macd > macd_signal:

            momentum_score += 10

        # ======================================
        # VOLUME CONFIRMATION
        # ======================================

        if volume_ratio > 1:

            volume_score += 5

        if volume_ratio > 1.5:

            volume_score += 5

        # ======================================
        # VOLATILITY
        # ======================================

        if volatility < 0.05:

            stability_score += 5

        if 0.02 <= atr_percent <= 0.08:

            stability_score += 5

        # ======================================
        # FINAL SCORE
        # ======================================

        score = trend_score + momentum_score + volume_score + stability_score

        score = min(score, 100)

        # ======================================
        # TREND STATUS
        # ======================================

        if score >= 80:

            trend_status = "STRONG BULLISH"

        elif score >= 65:

            trend_status = "BULLISH"

        elif score >= 50:

            trend_status = "NEUTRAL"

        else:

            trend_status = "WEAK"

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
            "score": score,
            "status": trend_status,
            "confidence": confidence,
            "close": round(close_price, 2),
            "ema20": round(ema20, 2),
            "ema50": round(ema50, 2),
            "ema200": round(ema200, 2),
            "rsi": round(rsi, 2),
            "adx": round(adx, 2),
            "macd": round(macd, 2),
            "volume_ratio": (volume_ratio),
            "atr_percent": (atr_percent),
        }

    except Exception as e:

        logger.error(f"Daily timeframe " f"error: {e}")

        return None
