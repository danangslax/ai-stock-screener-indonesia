import pandas as pd

from infrastructure.logger import logger

# ======================================
# BREAKOUT STRATEGY
# ======================================


def breakout_strategy(latest, df):

    try:

        # ======================================
        # BASIC DATA
        # ======================================

        price = float(latest["Close"])

        volume = float(latest["Volume"])

        ma20 = float(latest["MA20"])

        rsi = float(latest["RSI"])

        adx = float(latest["ADX"])

        atr = float(latest["ATR"])

        vol_ma20 = float(latest["VOL_MA20"])

        high_20 = float(latest["HIGH_20"])

        # ======================================
        # NAN VALIDATION
        # ======================================

        metrics = [price, volume, ma20, rsi, adx, atr, vol_ma20, high_20]

        if any(pd.isna(v) for v in metrics):

            return None

        # ======================================
        # METRICS
        # ======================================

        volume_ratio = round(volume / vol_ma20, 2)

        breakout_distance = round(((price - high_20) / high_20) * 100, 2)

        # ======================================
        # CONDITIONS
        # ======================================

        conditions = {
            # breakout
            "breakout": price >= high_20,
            # strong trend
            "trend": adx >= 25,
            # healthy RSI
            "momentum": 55 <= rsi <= 80,
            # volume expansion
            "volume": volume_ratio >= 1.5,
            # trend alignment
            "alignment": price > ma20,
            # healthy volatility
            "volatility": atr > 0,
        }

        # ======================================
        # WEIGHTED SCORE
        # ======================================

        score = 0

        if conditions["breakout"]:

            score += 25

        if conditions["trend"]:

            score += 20

        if conditions["momentum"]:

            score += 15

        if conditions["volume"]:

            score += 20

        if conditions["alignment"]:

            score += 10

        if conditions["volatility"]:

            score += 10

        # ======================================
        # STATUS
        # ======================================

        status = "PASS" if score >= 80 else "FAIL"

        # ======================================
        # RESULT
        # ======================================

        result = {
            "strategy": "BREAKOUT",
            "status": status,
            "score": score,
            "volume_ratio": (volume_ratio),
            "breakout_distance": (breakout_distance),
            "triggered_conditions": (sum(conditions.values())),
        }

        return result

    except Exception as e:

        logger.error(f"Breakout strategy " f"error: {e}")

        return None
