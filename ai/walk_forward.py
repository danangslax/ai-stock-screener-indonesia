import pandas as pd

# ======================================
# WALK FORWARD OPTIMIZATION ENGINE
# ======================================


def optimize_parameters(screener_df):

    try:

        if screener_df.empty:

            return {}

        df = screener_df.copy()

        # ======================================
        # REQUIRED COLUMNS
        # ======================================

        required = ["RSI", "ADX", "Volatility", "Confidence"]

        missing = [col for col in required if col not in df.columns]

        if missing:

            return {}

        # ======================================
        # HIGH CONFIDENCE
        # ======================================

        strong_df = df[df["Confidence"] >= 80]

        if strong_df.empty:

            return {}

        # ======================================
        # OPTIMAL RSI
        # ======================================

        optimal_rsi = round(strong_df["RSI"].mean(), 2)

        # ======================================
        # OPTIMAL ADX
        # ======================================

        optimal_adx = round(strong_df["ADX"].mean(), 2)

        # ======================================
        # OPTIMAL VOLATILITY
        # ======================================

        optimal_volatility = round(strong_df["Volatility"].mean(), 4)

        # ======================================
        # AI INSIGHT
        # ======================================

        insight = f"""
Optimal RSI:
{optimal_rsi}

Optimal ADX:
{optimal_adx}

Optimal Volatility:
{optimal_volatility}
"""

        return {
            "optimal_rsi": optimal_rsi,
            "optimal_adx": optimal_adx,
            "optimal_volatility": (optimal_volatility),
            "insight": insight,
        }

    except Exception as e:

        print(f"❌ Optimization error: " f"{e}")

        return {}
