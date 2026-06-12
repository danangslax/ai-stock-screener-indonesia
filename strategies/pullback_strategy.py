import pandas as pd

from infrastructure.logger import logger

# ======================================
# PULLBACK STRATEGY
# ======================================


def pullback_strategy(latest, df):

    try:

        # ======================================
        # BASIC DATA
        # ======================================

        price = float(latest["Close"])

        ma20 = float(latest["MA20"])

        ema20 = float(latest["EMA20"])

        ema50 = float(latest["EMA50"])

        rsi = float(latest["RSI"])

        adx = float(latest["ADX"])

        atr = float(latest["ATR"])

        volatility = float(latest["VOLATILITY"])

        volume = float(latest["Volume"])

        vol_ma20 = float(latest["VOL_MA20"])

        # ======================================
        # NAN VALIDATION
        # ======================================

        metrics = [
            price,
            ma20,
            ema20,
            ema50,
            rsi,
            adx,
            atr,
            volatility,
            volume,
            vol_ma20,
        ]

        if any(pd.isna(v) for v in metrics):

            return None

        # ======================================
        # ZERO VALIDATION
        # ======================================

        if ma20 <= 0:

            return None

        if vol_ma20 <= 0:

            return None

        # ======================================
        # DISTANCE FROM MA20
        # ======================================

        distance_ma20 = round(abs((price - ma20) / ma20), 4)

        # ======================================
        # VOLUME RATIO
        # ======================================

        volume_ratio = round(volume / vol_ma20, 2)

        # ======================================
        # CONDITIONS
        # ======================================

        conditions = {
            # healthy trend
            "trend": ema20 > ema50,
            # near MA20 pullback
            "pullback_zone": distance_ma20 <= 0.03,
            # healthy RSI
            "momentum": 50 <= rsi <= 65,
            # trend strength
            "trend_strength": adx >= 20,
            # controlled volatility
            "volatility": volatility < 0.05,
            # healthy ATR
            "healthy_atr": atr > 0,
            # volume contraction
            "volume_contraction": volume_ratio <= 1.2,
        }

        # ======================================
        # WEIGHTED SCORE
        # ======================================

        score = 0

        if conditions["trend"]:

            score += 25

        if conditions["pullback_zone"]:

            score += 25

        if conditions["momentum"]:

            score += 15

        if conditions["trend_strength"]:

            score += 15

        if conditions["volatility"]:

            score += 10

        if conditions["healthy_atr"]:

            score += 5

        if conditions["volume_contraction"]:

            score += 5

        # ======================================
        # STATUS
        # ======================================

        status = "PASS" if score >= 80 else "FAIL"

        # ======================================
        # RISK PROFILE
        # ======================================

        risk_profile = "LOW"

        if volatility > 0.04:

            risk_profile = "MEDIUM"

        # ======================================
        # RESULT
        # ======================================

        result = {
            "strategy": "PULLBACK",
            "status": status,
            "score": score,
            "distance_ma20": (round(distance_ma20 * 100, 2)),
            "volume_ratio": (volume_ratio),
            "risk_profile": (risk_profile),
            "triggered_conditions": (sum(conditions.values())),
        }

        return result

    except Exception as e:

        logger.error(f"Pullback strategy " f"error: {e}")

        return None
