# ======================================
# TRADE PLAN ENGINE
# ======================================


def generate_trade_plan(price, atr=None, risk_percent=2, reward_ratio=2):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if price <= 0:

            raise ValueError("Invalid price")

        # ======================================
        # ATR FALLBACK
        # ======================================

        # default ATR = 5% price
        if atr is None or atr <= 0:

            atr = price * 0.05

        # ======================================
        # ENTRY
        # ======================================

        entry = round(price, 2)

        # ======================================
        # STOP LOSS
        # ======================================

        stop_loss = round(entry - (2 * atr), 2)

        # ======================================
        # TAKE PROFIT
        # ======================================

        take_profit = round(entry + (reward_ratio * (entry - stop_loss)), 2)

        # ======================================
        # RISK CALCULATION
        # ======================================

        risk = round(entry - stop_loss, 2)

        reward = round(take_profit - entry, 2)

        # ======================================
        # RISK REWARD
        # ======================================

        if risk <= 0:

            rr_ratio = 0

        else:

            rr_ratio = round(reward / risk, 2)

        # ======================================
        # POSITION RISK %
        # ======================================

        position_risk = round((risk / entry) * 100, 2)

        # ======================================
        # TRADE QUALITY
        # ======================================

        if rr_ratio >= 3:

            quality = "EXCELLENT"

        elif rr_ratio >= 2:

            quality = "GOOD"

        elif rr_ratio >= 1.5:

            quality = "MODERATE"

        else:

            quality = "WEAK"

        # ======================================
        # RETURN DATA
        # ======================================

        return {
            "entry": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "risk": risk,
            "reward": reward,
            "risk_reward": rr_ratio,
            "position_risk_percent": (position_risk),
            "quality": quality,
        }

    except Exception as e:

        print(f"❌ Trade Plan Error: {e}")

        return {
            "entry": 0,
            "stop_loss": 0,
            "take_profit": 0,
            "risk": 0,
            "reward": 0,
            "risk_reward": 0,
            "position_risk_percent": 0,
            "quality": "ERROR",
        }
