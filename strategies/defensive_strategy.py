import pandas as pd

from infrastructure.logger import logger

# ======================================
# DEFENSIVE STRATEGY
# ======================================


def defensive_strategy(latest, df):

    try:

        # ======================================
        # BASIC DATA
        # ======================================

        volatility = float(latest["VOLATILITY"])

        rsi = float(latest["RSI"])

        ema20 = float(latest["EMA20"])

        ema50 = float(latest["EMA50"])

        atr = float(latest["ATR"])

        volume = float(latest["Volume"])

        vol_ma20 = float(latest["VOL_MA20"])

        # ======================================
        # NAN VALIDATION
        # ======================================

        metrics = [volatility, rsi, ema20, ema50, atr, volume, vol_ma20]

        if any(pd.isna(v) for v in metrics):

            return None

        # ======================================
        # VOLUME RATIO
        # ======================================

        if vol_ma20 <= 0:

            return None

        relative_volume = round(volume / vol_ma20, 2)

        # ======================================
        # CONDITIONS
        # ======================================

        conditions = {
            # low volatility
            "low_volatility": volatility < 0.04,
            # stable RSI
            "stable_rsi": 50 <= rsi <= 70,
            # trend stability
            "trend_alignment": ema20 > ema50,
            # healthy ATR
            "healthy_atr": atr > 0,
            # decent volume
            "volume_support": relative_volume >= 1,
        }

        # ======================================
        # WEIGHTED SCORE
        # ======================================

        score = 0

        if conditions["low_volatility"]:

            score += 30

        if conditions["stable_rsi"]:

            score += 20

        if conditions["trend_alignment"]:

            score += 25

        if conditions["healthy_atr"]:

            score += 10

        if conditions["volume_support"]:

            score += 15

        # ======================================
        # STATUS
        # ======================================

        status = "PASS" if score >= 75 else "FAIL"

        # ======================================
        # RISK PROFILE
        # ======================================

        risk_profile = "LOW"

        if volatility > 0.03:

            risk_profile = "MEDIUM"

        # ======================================
        # RESULT
        # ======================================

        result = {
            "strategy": "DEFENSIVE",
            "status": status,
            "score": score,
            "risk_profile": (risk_profile),
            "relative_volume": (relative_volume),
            "triggered_conditions": (sum(conditions.values())),
        }

        return result

    except Exception as e:

        logger.error(f"Defensive strategy " f"error: {e}")

        return None
