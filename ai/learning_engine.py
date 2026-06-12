import pandas as pd

# ======================================
# AI LEARNING ENGINE
# ======================================


def analyze_learning_data(journal_data):

    try:

        if not journal_data:

            return pd.DataFrame()

        df = pd.DataFrame(journal_data)

        # ======================================
        # REQUIRED COLUMNS
        # ======================================

        required_columns = ["strategy", "market_regime", "confidence", "result"]

        missing = [col for col in required_columns if col not in df.columns]

        if missing:

            return pd.DataFrame()

        # ======================================
        # CONVERT RESULT
        # ======================================

        df["is_win"] = df["result"].astype(str).str.contains("+")

        # ======================================
        # GROUP ANALYSIS
        # ======================================

        grouped = (
            df.groupby(["strategy", "market_regime"])
            .agg({"confidence": "mean", "is_win": "mean"})
            .reset_index()
        )

        # ======================================
        # CLEAN COLUMNS
        # ======================================

        grouped.columns = ["Strategy", "Market_Regime", "Average_Confidence", "Winrate"]

        # ======================================
        # PERCENTAGE
        # ======================================

        grouped["Winrate"] = grouped["Winrate"] * 100

        grouped["Average_Confidence"] = grouped["Average_Confidence"].round(2)

        grouped["Winrate"] = grouped["Winrate"].round(2)

        # ======================================
        # AI INSIGHT
        # ======================================

        insights = []

        for _, row in grouped.iterrows():

            strategy = row["Strategy"]

            regime = row["Market_Regime"]

            winrate = row["Winrate"]

            if winrate >= 70:

                insight = f"{strategy} works VERY WELL " f"during {regime}"

            elif winrate >= 50:

                insight = f"{strategy} works reasonably " f"well during {regime}"

            else:

                insight = f"{strategy} underperforms " f"during {regime}"

            insights.append(insight)

        grouped["AI_Insight"] = insights

        # ======================================
        # SORT
        # ======================================

        grouped = grouped.sort_values(by="Winrate", ascending=False).reset_index(
            drop=True
        )

        return grouped

    except Exception as e:

        print(f"❌ Learning engine error: " f"{e}")

        return pd.DataFrame()
