import pandas as pd

from infrastructure.logger import logger

# ======================================
# AI META STRATEGY ENGINE
# ======================================


def adjust_confidence(base_confidence, strategy_name, market_regime, learning_df):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if learning_df.empty:

            return {
                "adjusted_confidence": (base_confidence),
                "adjustment": 0,
                "reason": ("No learning data"),
                "winrate": 0,
                "sample_size": 0,
                "performance": ("UNKNOWN"),
            }

        # ======================================
        # REQUIRED COLUMNS
        # ======================================

        required_columns = [
            "Strategy",
            "Market_Regime",
            "Winrate",
            "Total_Trades",
            "Performance",
        ]

        missing = [col for col in required_columns if col not in learning_df.columns]

        if missing:

            logger.warning(f"Meta strategy " f"missing columns: " f"{missing}")

            return {
                "adjusted_confidence": (base_confidence),
                "adjustment": 0,
                "reason": ("Invalid learning data"),
                "winrate": 0,
                "sample_size": 0,
                "performance": ("UNKNOWN"),
            }

        # ======================================
        # FILTER MATCHING PROFILE
        # ======================================

        filtered = learning_df[
            (learning_df["Strategy"] == strategy_name)
            & (learning_df["Market_Regime"] == market_regime)
        ]

        # ======================================
        # NO MATCH
        # ======================================

        if filtered.empty:

            return {
                "adjusted_confidence": (base_confidence),
                "adjustment": 0,
                "reason": ("No matching data"),
                "winrate": 0,
                "sample_size": 0,
                "performance": ("UNKNOWN"),
            }

        # ======================================
        # BEST MATCH
        # ======================================

        row = filtered.iloc[0]

        # ======================================
        # DATA
        # ======================================

        winrate = float(row["Winrate"])

        total_trades = int(row["Total_Trades"])

        performance = str(row["Performance"])

        # ======================================
        # SAMPLE CONFIDENCE
        # ======================================

        sample_multiplier = 1.0

        if total_trades < 10:

            sample_multiplier = 0.5

        elif total_trades < 20:

            sample_multiplier = 0.75

        # ======================================
        # ADJUSTMENT
        # ======================================

        adjustment = 0

        reason = ""

        # ======================================
        # ELITE PERFORMANCE
        # ======================================

        if winrate >= 75:

            adjustment = int(10 * sample_multiplier)

            reason = (
                f"{strategy_name} " f"performs VERY WELL " f"during " f"{market_regime}"
            )

        # ======================================
        # STRONG PERFORMANCE
        # ======================================

        elif winrate >= 60:

            adjustment = int(5 * sample_multiplier)

            reason = f"{strategy_name} " f"performs well " f"during " f"{market_regime}"

        # ======================================
        # WEAK PERFORMANCE
        # ======================================

        elif winrate < 40:

            adjustment = int(-10 * sample_multiplier)

            reason = f"{strategy_name} " f"underperforms " f"during " f"{market_regime}"

        # ======================================
        # NEUTRAL
        # ======================================

        else:

            adjustment = 0

            reason = (
                f"{strategy_name} "
                f"performance neutral "
                f"during "
                f"{market_regime}"
            )

        # ======================================
        # ADJUST CONFIDENCE
        # ======================================

        adjusted = base_confidence + adjustment

        # ======================================
        # LIMIT
        # ======================================

        adjusted = max(0, min(100, adjusted))

        logger.info(
            f"Meta AI | "
            f"{strategy_name} | "
            f"{market_regime} | "
            f"WR={winrate}% | "
            f"Trades={total_trades} | "
            f"Adj={adjustment}"
        )

        # ======================================
        # RESULT
        # ======================================

        return {
            "adjusted_confidence": (adjusted),
            "adjustment": (adjustment),
            "reason": (reason),
            "winrate": (winrate),
            "sample_size": (total_trades),
            "performance": (performance),
            "sample_multiplier": (sample_multiplier),
        }

    except Exception as e:

        logger.error(f"Meta strategy " f"error: {e}")

        return {
            "adjusted_confidence": (base_confidence),
            "adjustment": 0,
            "reason": "Error",
            "winrate": 0,
            "sample_size": 0,
            "performance": "ERROR",
        }
