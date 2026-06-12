import pandas as pd

from infrastructure.logger import logger

# ======================================
# MARKET SIMULATOR ENGINE
# ======================================


def simulate_market_conditions(screener_df):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if screener_df.empty:

            logger.warning("Market simulator " "received empty dataframe")

            return pd.DataFrame()

        # ======================================
        # REQUIRED COLUMNS
        # ======================================

        required_columns = [
            "Confidence",
            "Strategy",
            "RS_Status",
        ]

        missing = [col for col in required_columns if col not in screener_df.columns]

        if missing:

            logger.warning(f"Simulator missing " f"columns: {missing}")

            return pd.DataFrame()

        # ======================================
        # MARKET REGIMES
        # ======================================

        market_regimes = [
            "STRONG_BULL",
            "BULL",
            "SIDEWAYS",
            "BEARISH",
            "PANIC",
            "RECOVERY",
        ]

        # ======================================
        # RESULT CONTAINER
        # ======================================

        simulations = []

        # ======================================
        # LOOP REGIMES
        # ======================================

        for regime in market_regimes:

            df = screener_df.copy()

            # ======================================
            # BASE SCORE
            # ======================================

            base_score = float(df["Confidence"].mean())

            # ======================================
            # REGIME ADJUSTMENT
            # ======================================

            regime_adjustment = 0

            if regime == "STRONG_BULL":

                regime_adjustment = 15

            elif regime == "BULL":

                regime_adjustment = 10

            elif regime == "RECOVERY":

                regime_adjustment = 5

            elif regime == "SIDEWAYS":

                regime_adjustment = -5

            elif regime == "BEARISH":

                regime_adjustment = -15

            elif regime == "PANIC":

                regime_adjustment = -25

            # ======================================
            # STRATEGY EFFECT
            # ======================================

            strategy_bonus = 0

            breakout_count = len(df[df["Strategy"] == "BREAKOUT"])

            defensive_count = len(df[df["Strategy"] == "DEFENSIVE"])

            pullback_count = len(df[df["Strategy"] == "PULLBACK"])

            total = len(df)

            if total > 0:

                breakout_ratio = breakout_count / total

                defensive_ratio = defensive_count / total

                pullback_ratio = pullback_count / total

            else:

                breakout_ratio = 0
                defensive_ratio = 0
                pullback_ratio = 0

            # ======================================
            # REGIME STRATEGY LOGIC
            # ======================================

            if regime in [
                "STRONG_BULL",
                "BULL",
            ]:

                strategy_bonus += breakout_ratio * 15

                strategy_bonus += pullback_ratio * 8

            elif regime in [
                "BEARISH",
                "PANIC",
            ]:

                strategy_bonus += defensive_ratio * 15

                strategy_bonus -= breakout_ratio * 10

            elif regime == "SIDEWAYS":

                strategy_bonus += defensive_ratio * 8

            # ======================================
            # RELATIVE STRENGTH BONUS
            # ======================================

            market_leaders = len(df[df["RS_Status"] == "MARKET LEADER"])

            rs_bonus = 0

            if total > 0:

                rs_bonus = (market_leaders / total) * 10

            # ======================================
            # FINAL SCORE
            # ======================================

            final_score = base_score + regime_adjustment + strategy_bonus + rs_bonus

            # ======================================
            # LIMIT
            # ======================================

            final_score = max(0, min(100, final_score))

            # ======================================
            # SURVIVABILITY STATUS
            # ======================================

            if final_score >= 85:

                status = "ELITE"

            elif final_score >= 70:

                status = "STRONG"

            elif final_score >= 55:

                status = "STABLE"

            else:

                status = "WEAK"

            # ======================================
            # SURVIVABILITY SCORE
            # ======================================

            survivability = round((final_score / 100) * 10, 2)

            # ======================================
            # SAVE RESULT
            # ======================================

            simulations.append(
                {
                    "Market_Regime": (regime),
                    "Base_Score": round(base_score, 2),
                    "Regime_Adjustment": round(regime_adjustment, 2),
                    "Strategy_Bonus": round(strategy_bonus, 2),
                    "RS_Bonus": round(rs_bonus, 2),
                    "Simulation_Score": round(final_score, 2),
                    "Survivability": (survivability),
                    "Status": (status),
                }
            )

        # ======================================
        # FINAL DATAFRAME
        # ======================================

        result_df = pd.DataFrame(simulations)

        # ======================================
        # SORT
        # ======================================

        result_df = result_df.sort_values(
            by="Simulation_Score", ascending=False
        ).reset_index(drop=True)

        logger.info("Market simulation complete")

        return result_df

    except Exception as e:

        logger.error(f"Simulation " f"error: {e}")

        return pd.DataFrame()
