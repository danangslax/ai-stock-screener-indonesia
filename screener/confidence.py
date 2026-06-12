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

        confidence = 0

        # ======================================
        # WEEKLY TREND
        # ======================================

        if weekly_analysis:

            if weekly_analysis["status"] == "STRONG":

                confidence += 20

            elif weekly_analysis["status"] == "GOOD":

                confidence += 10

        # ======================================
        # DAILY STRUCTURE
        # ======================================

        if daily_analysis:

            confidence += min(int(daily_analysis["score"] * 0.2), 20)

        # ======================================
        # RELATIVE STRENGTH
        # ======================================

        if rs_analysis:

            if rs_analysis["status"] == "MARKET LEADER":

                confidence += 20

            elif rs_analysis["status"] == "STRONG":

                confidence += 10

        # ======================================
        # STRATEGY QUALITY
        # ======================================

        if strategy_analysis:

            confidence += min(int(strategy_analysis["score"] * 0.15), 15)

        # ======================================
        # MARKET REGIME
        # ======================================

        bullish_regimes = ["STRONG_BULL", "BULL", "RECOVERY"]

        if market_status in bullish_regimes:

            confidence += 15

        elif market_status in ["ACCUMULATION", "SIDEWAYS"]:

            confidence += 8

        # ======================================
        # VOLUME CONFIRMATION
        # ======================================

        relative_volume = latest["Volume"] / latest["VOL_MA20"]

        if relative_volume >= 2:

            confidence += 10

        elif relative_volume >= 1.2:

            confidence += 5

        # ======================================
        # LIMIT
        # ======================================

        if confidence > 100:

            confidence = 100

        # ======================================
        # SIGNAL QUALITY
        # ======================================

        if confidence >= 85:

            quality = "HIGH"

        elif confidence >= 70:

            quality = "MEDIUM"

        else:

            quality = "LOW"

        return {"confidence": confidence, "quality": quality}

    except Exception as e:

        print(f"❌ Confidence error: " f"{e}")

        return {"confidence": 0, "quality": "LOW"}
