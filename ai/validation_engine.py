import pandas as pd

# ======================================
# VALIDATION ENGINE
# ======================================


def validate_strategy_by_regime(trades):

    try:

        if not trades:

            return pd.DataFrame()

        df = pd.DataFrame(trades)

        # ======================================
        # REQUIRED COLUMNS
        # ======================================

        required = ["market_regime", "strategy", "profit_loss"]

        missing = [col for col in required if col not in df.columns]

        if missing:

            return pd.DataFrame()

        # ======================================
        # WIN COLUMN
        # ======================================

        df["is_win"] = df["profit_loss"] > 0

        # ======================================
        # GROUP ANALYSIS
        # ======================================

        grouped = (
            df.groupby(["market_regime", "strategy"])
            .agg({"profit_loss": ["mean", "sum"], "is_win": "mean"})
            .reset_index()
        )

        # ======================================
        # FLATTEN COLUMNS
        # ======================================

        grouped.columns = [
            "Market_Regime",
            "Strategy",
            "Average_PnL",
            "Total_PnL",
            "Winrate",
        ]

        # ======================================
        # CLEAN DATA
        # ======================================

        grouped["Average_PnL"] = grouped["Average_PnL"].round(2)

        grouped["Total_PnL"] = grouped["Total_PnL"].round(2)

        grouped["Winrate"] = (grouped["Winrate"] * 100).round(2)

        # ======================================
        # VALIDATION SCORE
        # ======================================

        grouped["Validation_Score"] = (
            (grouped["Winrate"] * 0.6) + (grouped["Average_PnL"] * 0.4)
        ).round(2)

        # ======================================
        # STATUS
        # ======================================

        status = []

        for _, row in grouped.iterrows():

            score = row["Validation_Score"]

            if score >= 70:

                label = "ROBUST"

            elif score >= 50:

                label = "STABLE"

            else:

                label = "WEAK"

            status.append(label)

        grouped["Status"] = status

        # ======================================
        # SORT
        # ======================================

        grouped = grouped.sort_values(
            by="Validation_Score", ascending=False
        ).reset_index(drop=True)

        return grouped

    except Exception as e:

        print(f"❌ Validation engine error: " f"{e}")

        return pd.DataFrame()
