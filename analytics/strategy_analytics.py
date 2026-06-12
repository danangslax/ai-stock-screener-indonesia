import pandas as pd

# ======================================
# STRATEGY PERFORMANCE ANALYTICS
# ======================================


def analyze_strategy_performance(trades):

    try:

        if not trades:

            return pd.DataFrame()

        df = pd.DataFrame(trades)

        # ======================================
        # VALIDATION
        # ======================================

        if "strategy" not in df.columns:

            return pd.DataFrame()

        if "pnl" not in df.columns:

            return pd.DataFrame()

        # ======================================
        # GROUP STRATEGIES
        # ======================================

        grouped = df.groupby("strategy").agg({"pnl": ["count", "sum", "mean"]})

        grouped.columns = ["Total_Trades", "Total_PnL", "Average_PnL"]

        grouped = grouped.reset_index()

        # ======================================
        # WINRATE
        # ======================================

        winrates = []

        for strategy in grouped["strategy"]:

            strategy_df = df[df["strategy"] == strategy]

            wins = len(strategy_df[strategy_df["pnl"] > 0])

            total = len(strategy_df)

            winrate = round((wins / total) * 100, 2)

            winrates.append(winrate)

        grouped["Winrate"] = winrates

        # ======================================
        # SORT
        # ======================================

        grouped = grouped.sort_values(by="Total_PnL", ascending=False).reset_index(
            drop=True
        )

        return grouped

    except Exception as e:

        print(f"❌ Strategy analytics error: " f"{e}")

        return pd.DataFrame()
