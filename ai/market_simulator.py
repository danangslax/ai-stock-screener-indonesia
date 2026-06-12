import pandas as pd

# ======================================
# MARKET SIMULATOR ENGINE
# ======================================


def simulate_market_conditions(screener_df):

    try:

        if screener_df.empty:

            return pd.DataFrame()

        simulations = []

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
        # LOOP REGIMES
        # ======================================

        for regime in market_regimes:

            df = screener_df.copy()

            # ======================================
            # BASE SCORE
            # ======================================

            score = float(df["Confidence"].mean())

            # ======================================
            # STRATEGY EFFECT
            # ======================================

            adjustment = 0

            if regime == "STRONG_BULL":

                adjustment = 15

            elif regime == "BULL":

                adjustment = 10

            elif regime == "RECOVERY":

                adjustment = 5

            elif regime == "SIDEWAYS":

                adjustment = -5

            elif regime == "BEARISH":

                adjustment = -15

            elif regime == "PANIC":

                adjustment = -25

            # ======================================
            # FINAL SCORE
            # ======================================

            final_score = score + adjustment

            # ======================================
            # LIMIT
            # ======================================

            final_score = max(0, min(100, final_score))

            # ======================================
            # SURVIVAL STATUS
            # ======================================

            if final_score >= 80:

                status = "EXCELLENT"

            elif final_score >= 65:

                status = "GOOD"

            elif final_score >= 50:

                status = "AVERAGE"

            else:

                status = "WEAK"

            # ======================================
            # SAVE RESULT
            # ======================================

            simulations.append(
                {
                    "Market_Regime": regime,
                    "Simulation_Score": round(final_score, 2),
                    "Status": status,
                }
            )

        # ======================================
        # FINAL DATAFRAME
        # ======================================

        result_df = pd.DataFrame(simulations)

        return result_df

    except Exception as e:

        print(f"❌ Simulation error: " f"{e}")

        return pd.DataFrame()
