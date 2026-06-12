import pandas as pd

from infrastructure.logger import logger

# ======================================
# VALIDATION ENGINE
# ======================================


def validate_strategy_by_regime(trades, minimum_sample=5):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if not trades:

            logger.warning("Validation engine " "received empty trades")

            return pd.DataFrame()

        # ======================================
        # DATAFRAME
        # ======================================

        df = pd.DataFrame(trades)

        # ======================================
        # REQUIRED COLUMNS
        # ======================================

        required = ["market_regime", "strategy", "profit_loss"]

        missing = [col for col in required if col not in df.columns]

        if missing:

            logger.warning(f"Validation engine " f"missing columns: " f"{missing}")

            return pd.DataFrame()

        # ======================================
        # CLEAN PNL
        # ======================================

        df["profit_loss"] = pd.to_numeric(df["profit_loss"], errors="coerce")

        df = df.dropna(subset=["profit_loss"])

        if df.empty:

            return pd.DataFrame()

        # ======================================
        # WIN / LOSS
        # ======================================

        df["is_win"] = df["profit_loss"] > 0

        # ======================================
        # GROUP ANALYSIS
        # ======================================

        grouped = (
            df.groupby(["market_regime", "strategy"])
            .agg(
                {
                    "profit_loss": ["mean", "sum", "count"],
                    "is_win": "mean",
                }
            )
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
            "Total_Trades",
            "Winrate",
        ]

        # ======================================
        # FILTER SAMPLE SIZE
        # ======================================

        grouped = grouped[grouped["Total_Trades"] >= minimum_sample]

        if grouped.empty:

            logger.warning("No valid validation samples")

            return pd.DataFrame()

        # ======================================
        # CLEAN DATA
        # ======================================

        grouped["Average_PnL"] = grouped["Average_PnL"].round(2)

        grouped["Total_PnL"] = grouped["Total_PnL"].round(2)

        grouped["Winrate"] = (grouped["Winrate"] * 100).round(2)

        # ======================================
        # EXPECTANCY
        # ======================================

        grouped["Expectancy"] = (
            grouped["Average_PnL"] * grouped["Winrate"] / 100
        ).round(2)

        # ======================================
        # VALIDATION SCORE
        # ======================================

        validation_scores = []

        statuses = []

        insights = []

        # ======================================
        # LOOP
        # ======================================

        for _, row in grouped.iterrows():

            winrate = row["Winrate"]

            expectancy = row["Expectancy"]

            total_pnl = row["Total_PnL"]

            total_trades = row["Total_Trades"]

            strategy = row["Strategy"]

            regime = row["Market_Regime"]

            # ======================================
            # SCORE
            # ======================================

            score = 0

            # Winrate
            score += min(winrate * 0.5, 50)

            # Expectancy
            if expectancy > 0:

                score += min(expectancy * 2, 30)

            # Consistency
            if total_trades >= 20:

                score += 10

            if total_pnl > 0:

                score += 10

            score = round(min(score, 100), 2)

            validation_scores.append(score)

            # ======================================
            # STATUS
            # ======================================

            if score >= 80:

                label = "ROBUST"

                insight = f"{strategy} " f"very stable during " f"{regime}"

            elif score >= 60:

                label = "STABLE"

                insight = f"{strategy} " f"reasonably effective " f"during {regime}"

            else:

                label = "WEAK"

                insight = f"{strategy} " f"underperforms during " f"{regime}"

            # ======================================
            # LOW SAMPLE WARNING
            # ======================================

            if total_trades < 10:

                insight += " | low sample size"

            statuses.append(label)

            insights.append(insight)

        # ======================================
        # SAVE RESULTS
        # ======================================

        grouped["Validation_Score"] = validation_scores

        grouped["Status"] = statuses

        grouped["AI_Insight"] = insights

        # ======================================
        # SORT
        # ======================================

        grouped = grouped.sort_values(
            by=[
                "Validation_Score",
                "Winrate",
                "Expectancy",
            ],
            ascending=False,
        ).reset_index(drop=True)

        logger.info(f"Validation engine " f"analyzed " f"{len(grouped)} " f"profiles")

        return grouped

    except Exception as e:

        logger.error(f"Validation engine " f"error: {e}")

        return pd.DataFrame()
