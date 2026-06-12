from infrastructure.logger import logger

# ======================================
# DEFAULT RESULT
# ======================================

DEFAULT_RESULT = {
    "entry": 0,
    "stop_loss": 0,
    "take_profit": 0,
    "risk": 0,
    "reward": 0,
    "risk_reward": 0,
    "position_risk_percent": 0,
    "expected_return_percent": 0,
    "setup_quality": "ERROR",
    "trade_score": 0,
    "execution_recommendation": "AVOID",
    "survivability_score": 0,
}

# ======================================
# TRADE PLAN ENGINE
# ======================================


def generate_trade_plan(
    price,
    atr=None,
    confidence=50,
    market_regime="SIDEWAYS",
    risk_percent=2,
    reward_ratio=2,
):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if price <= 0:

            raise ValueError("Invalid price")

        # ======================================
        # ATR FALLBACK
        # ======================================

        if atr is None or atr <= 0:

            atr = price * 0.05

        # ======================================
        # MARKET REGIME ADAPTATION
        # ======================================

        atr_multiplier = 2

        adjusted_reward_ratio = reward_ratio

        if market_regime == "STRONG_BULL":

            adjusted_reward_ratio = 3

            atr_multiplier = 2.5

        elif market_regime == "BULL":

            adjusted_reward_ratio = 2.5

        elif market_regime == "RECOVERY":

            adjusted_reward_ratio = 2.2

        elif market_regime == "SIDEWAYS":

            adjusted_reward_ratio = 1.8

        elif market_regime == "BEARISH":

            adjusted_reward_ratio = 1.5

            atr_multiplier = 1.5

        elif market_regime == "PANIC":

            adjusted_reward_ratio = 1.2

            atr_multiplier = 1

        # ======================================
        # ENTRY
        # ======================================

        entry = round(price, 2)

        # ======================================
        # STOP LOSS
        # ======================================

        stop_loss = round(entry - (atr_multiplier * atr), 2)

        # ======================================
        # TAKE PROFIT
        # ======================================

        take_profit = round(entry + (adjusted_reward_ratio * (entry - stop_loss)), 2)

        # ======================================
        # RISK CALCULATION
        # ======================================

        risk = round(entry - stop_loss, 2)

        reward = round(take_profit - entry, 2)

        # ======================================
        # RISK REWARD
        # ======================================

        rr_ratio = 0

        if risk > 0:

            rr_ratio = round(reward / risk, 2)

        # ======================================
        # POSITION RISK %
        # ======================================

        position_risk = round((risk / entry) * 100, 2)

        # ======================================
        # EXPECTED RETURN %
        # ======================================

        expected_return_percent = round((reward / entry) * 100, 2)

        # ======================================
        # VOLATILITY RISK
        # ======================================

        atr_percent = round((atr / entry) * 100, 2)

        # ======================================
        # SETUP QUALITY
        # ======================================

        setup_quality = "C"

        if rr_ratio >= 3 and confidence >= 85:

            setup_quality = "A+"

        elif rr_ratio >= 2.5 and confidence >= 75:

            setup_quality = "A"

        elif rr_ratio >= 2 and confidence >= 65:

            setup_quality = "B"

        # ======================================
        # TRADE SCORE
        # ======================================

        trade_score = round(
            (rr_ratio * 25) + (confidence * 0.5) + (max(0, 15 - position_risk) * 2), 2
        )

        trade_score = min(trade_score, 100)

        # ======================================
        # SURVIVABILITY SCORE
        # ======================================

        survivability_score = 100

        # Risk penalty
        survivability_score -= position_risk * 2

        # Volatility penalty
        survivability_score -= atr_percent * 1.5

        # Panic market penalty
        if market_regime == "PANIC":

            survivability_score -= 25

        survivability_score = max(0, round(survivability_score, 2))

        # ======================================
        # EXECUTION RECOMMENDATION
        # ======================================

        execution_recommendation = "AVOID"

        if setup_quality == "A+" and survivability_score >= 70:

            execution_recommendation = "FULL SIZE"

        elif setup_quality in ["A", "B"] and survivability_score >= 50:

            execution_recommendation = "HALF SIZE"

        # ======================================
        # INSTITUTIONAL SAFETY
        # ======================================

        if position_risk > 15:

            execution_recommendation = "AVOID"

        if market_regime == "PANIC":

            execution_recommendation = "AVOID"

        logger.info("Trade plan generated")

        # ======================================
        # RETURN RESULT
        # ======================================

        return {
            "entry": (entry),
            "stop_loss": (stop_loss),
            "take_profit": (take_profit),
            "risk": (risk),
            "reward": (reward),
            "risk_reward": (rr_ratio),
            "position_risk_percent": (position_risk),
            "expected_return_percent": (expected_return_percent),
            "atr_percent": (atr_percent),
            "setup_quality": (setup_quality),
            "trade_score": (trade_score),
            "execution_recommendation": (execution_recommendation),
            "survivability_score": (survivability_score),
        }

    except Exception as e:

        logger.error(f"Trade Plan " f"Error: {e}")

        return DEFAULT_RESULT.copy()
