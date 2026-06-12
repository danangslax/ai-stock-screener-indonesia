import pandas as pd

from infrastructure.logger import logger

# ======================================
# AI SIGNAL CONFIDENCE ENGINE
# ======================================


def calculate_confidence(
    market_status,
    weekly_analysis,
    daily_analysis,
    rs_analysis,
    strategy_analysis,
    latest,
):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if latest is None:

            return {"confidence": 0, "quality": "INVALID"}

        # ======================================
        # SCORE CONTAINERS
        # ======================================

        trend_confidence = 0

        relative_strength_confidence = 0

        strategy_confidence = 0

        market_confidence = 0

        volume_confidence = 0

        penalty = 0

        # ======================================
        # WEEKLY TREND
        # ======================================

        if weekly_analysis:

            weekly_status = weekly_analysis.get("status", "WEAK")

            if weekly_status == "STRONG":

                trend_confidence += 20

            elif weekly_status == "GOOD":

                trend_confidence += 10

        # ======================================
        # DAILY STRUCTURE
        # ======================================

        if daily_analysis:

            daily_score = daily_analysis.get("score", 0)

            trend_confidence += min(int(daily_score * 0.2), 20)

        # ======================================
        # RELATIVE STRENGTH
        # ======================================

        if rs_analysis:

            rs_status = rs_analysis.get("status", "WEAK")

            if rs_status == "MARKET LEADER":

                relative_strength_confidence += 20

            elif rs_status == "STRONG":

                relative_strength_confidence += 10

            elif rs_status == "WEAK":

                penalty += 10

        # ======================================
        # STRATEGY QUALITY
        # ======================================

        if strategy_analysis:

            strategy_score = strategy_analysis.get("score", 0)

            strategy_name = strategy_analysis.get("strategy", "UNKNOWN")

            strategy_confidence += min(int(strategy_score * 0.15), 15)

        else:

            strategy_name = "UNKNOWN"

        # ======================================
        # MARKET REGIME
        # ======================================

        bullish_regimes = ["STRONG_BULL", "BULL", "RECOVERY"]

        neutral_regimes = ["ACCUMULATION", "SIDEWAYS"]

        bearish_regimes = ["DISTRIBUTION", "PANIC", "BEARISH"]

        if market_status in bullish_regimes:

            market_confidence += 15

        elif market_status in neutral_regimes:

            market_confidence += 8

        elif market_status in bearish_regimes:

            penalty += 15

        # ======================================
        # STRATEGY-REGIME FIT
        # ======================================

        if strategy_name == "BREAKOUT" and market_status in bearish_regimes:

            penalty += 20

        if strategy_name == "DEFENSIVE" and market_status in bullish_regimes:

            penalty += 5

        # ======================================
        # VOLUME CONFIRMATION
        # ======================================

        volume = latest.get("Volume", 0)

        vol_ma20 = latest.get("VOL_MA20", 0)

        # ======================================
        # VALIDATION
        # ======================================

        metrics = [volume, vol_ma20]

        if any(pd.isna(v) for v in metrics):

            return {"confidence": 0, "quality": "INVALID"}

        if vol_ma20 > 0:

            relative_volume = volume / vol_ma20

        else:

            relative_volume = 0

        # ======================================
        # VOLUME CONFIDENCE
        # ======================================

        if relative_volume >= 2:

            volume_confidence += 10

        elif relative_volume >= 1.2:

            volume_confidence += 5

        # ======================================
        # FINAL CONFIDENCE
        # ======================================

        raw_confidence = (
            trend_confidence
            + relative_strength_confidence
            + strategy_confidence
            + market_confidence
            + volume_confidence
            - penalty
        )

        confidence = max(0, min(100, raw_confidence))

        # ======================================
        # QUALITY
        # ======================================

        quality = "LOW"

        if confidence >= 85:

            quality = "ELITE"

        elif confidence >= 70:

            quality = "HIGH"

        elif confidence >= 55:

            quality = "MEDIUM"

        elif confidence < 40:

            quality = "AVOID"

        # ======================================
        # RESULT
        # ======================================

        return {
            "confidence": confidence,
            "quality": quality,
            "trend_confidence": (trend_confidence),
            "relative_strength_confidence": (relative_strength_confidence),
            "strategy_confidence": (strategy_confidence),
            "market_confidence": (market_confidence),
            "volume_confidence": (volume_confidence),
            "penalty": penalty,
        }

    except Exception as e:

        logger.error(f"Confidence " f"error: {e}")

        return {"confidence": 0, "quality": "ERROR"}
