import pandas as pd

# ======================================
# AI META STRATEGY ENGINE
# ======================================


def adjust_confidence(base_confidence, strategy_name, market_regime, learning_df):

    try:

        if learning_df.empty:

            return {
                "adjusted_confidence": (base_confidence),
                "adjustment": 0,
                "reason": ("No learning data"),
            }

        # ======================================
        # FILTER DATA
        # ======================================

        filtered = learning_df[
            (learning_df["Strategy"] == strategy_name)
            & (learning_df["Market_Regime"] == market_regime)
        ]

        # ======================================
        # NO DATA
        # ======================================

        if filtered.empty:

            return {
                "adjusted_confidence": (base_confidence),
                "adjustment": 0,
                "reason": ("No matching data"),
            }

        row = filtered.iloc[0]

        winrate = float(row["Winrate"])

        adjustment = 0

        reason = ""

        # ======================================
        # STRONG PERFORMANCE
        # ======================================

        if winrate >= 75:

            adjustment = 10

            reason = (
                f"{strategy_name} performs " f"VERY WELL during " f"{market_regime}"
            )

        # ======================================
        # GOOD PERFORMANCE
        # ======================================

        elif winrate >= 60:

            adjustment = 5

            reason = f"{strategy_name} performs " f"well during " f"{market_regime}"

        # ======================================
        # BAD PERFORMANCE
        # ======================================

        elif winrate < 40:

            adjustment = -10

            reason = f"{strategy_name} performs " f"poorly during " f"{market_regime}"

        # ======================================
        # ADJUST CONFIDENCE
        # ======================================

        adjusted = base_confidence + adjustment

        # ======================================
        # LIMIT
        # ======================================

        if adjusted > 100:

            adjusted = 100

        if adjusted < 0:

            adjusted = 0

        return {
            "adjusted_confidence": adjusted,
            "adjustment": adjustment,
            "reason": reason,
        }

    except Exception as e:

        print(f"❌ Meta strategy error: " f"{e}")

        return {
            "adjusted_confidence": (base_confidence),
            "adjustment": 0,
            "reason": "Error",
        }
