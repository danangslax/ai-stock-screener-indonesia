import pandas as pd

from infrastructure.logger import logger

# ======================================
# AI LEARNING ENGINE
# ======================================


def analyze_learning_data(journal_data, minimum_sample=5):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if not journal_data:

            logger.warning("Learning engine " "received empty journal")

            return pd.DataFrame()

        # ======================================
        # DATAFRAME
        # ======================================

        df = pd.DataFrame(journal_data)

        # ======================================
        # REQUIRED COLUMNS
        # ======================================

        required_columns = ["strategy", "market_regime", "confidence", "result"]

        missing = [col for col in required_columns if col not in df.columns]

        if missing:

            logger.warning(f"Learning engine " f"missing columns: " f"{missing}")

            return pd.DataFrame()

        # ======================================
        # CLEAN CONFIDENCE
        # ======================================

        df["confidence"] = pd.to_numeric(df["confidence"], errors="coerce")

        df = df.dropna(subset=["confidence"])

        # ======================================
        # WIN DETECTION
        # ======================================

        df["result"] = df["result"].astype(str).str.strip()

        # ======================================
        # WIN / LOSS
        # ======================================

        df["is_win"] = df["result"].str.contains(r"\+", regex=True)

        # ======================================
        # SAMPLE SIZE
        # ======================================

        grouped = (
            df.groupby(["strategy", "market_regime"])
            .agg(
                {
                    "confidence": "mean",
                    "is_win": "mean",
                    "result": "count",
                }
            )
            .reset_index()
        )

        # ======================================
        # CLEAN COLUMNS
        # ======================================

        grouped.columns = [
            "Strategy",
            "Market_Regime",
            "Average_Confidence",
            "Winrate",
            "Total_Trades",
        ]

        # ======================================
        # FILTER MINIMUM SAMPLE
        # ======================================

        grouped = grouped[grouped["Total_Trades"] >= minimum_sample]

        if grouped.empty:

            logger.warning("No valid learning samples")

            return pd.DataFrame()

        # ======================================
        # PERCENTAGE
        # ======================================

        grouped["Winrate"] = grouped["Winrate"] * 100

        # ======================================
        # ROUNDING
        # ======================================

        grouped["Average_Confidence"] = grouped["Average_Confidence"].round(2)

        grouped["Winrate"] = grouped["Winrate"].round(2)

        # ======================================
        # AI INSIGHT
        # ======================================

        insights = []

        performance = []

        # ======================================
        # GENERATE INSIGHT
        # ======================================

        for _, row in grouped.iterrows():

            strategy = row["Strategy"]

            regime = row["Market_Regime"]

            winrate = row["Winrate"]

            total_trades = row["Total_Trades"]

            # ======================================
            # PERFORMANCE LEVEL
            # ======================================

            if winrate >= 75:

                level = "ELITE"

                insight = f"{strategy} performs " f"extremely well during " f"{regime}"

            elif winrate >= 60:

                level = "STRONG"

                insight = f"{strategy} works well " f"during {regime}"

            elif winrate >= 50:

                level = "NEUTRAL"

                insight = f"{strategy} is moderately " f"effective during {regime}"

            else:

                level = "WEAK"

                insight = f"{strategy} underperforms " f"during {regime}"

            # ======================================
            # SMALL SAMPLE WARNING
            # ======================================

            if total_trades < 10:

                insight += " | low sample size"

            insights.append(insight)

            performance.append(level)

        # ======================================
        # SAVE INSIGHTS
        # ======================================

        grouped["Performance"] = performance

        grouped["AI_Insight"] = insights

        # ======================================
        # SORT
        # ======================================

        grouped = grouped.sort_values(
            by=[
                "Performance",
                "Winrate",
                "Average_Confidence",
            ],
            ascending=False,
        ).reset_index(drop=True)

        logger.info(
            f"Learning engine " f"analyzed " f"{len(grouped)} " f"strategy profiles"
        )

        return grouped

    except Exception as e:

        logger.error(f"Learning engine " f"error: {e}")

        return pd.DataFrame()
