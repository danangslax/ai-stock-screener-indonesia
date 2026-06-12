import pandas as pd
import numpy as np

# ======================================
# PERFORMANCE ANALYTICS ENGINE
# ======================================


def analyze_performance(trades):

    try:

        if not trades:

            return {}

        df = pd.DataFrame(trades)

        # ======================================
        # REQUIRED COLUMNS
        # ======================================

        required_columns = ["profit_loss"]

        missing = [col for col in required_columns if col not in df.columns]

        if missing:

            return {}

        # ======================================
        # TOTAL TRADES
        # ======================================

        total_trades = len(df)

        # ======================================
        # WIN / LOSS
        # ======================================

        wins = df[df["profit_loss"] > 0]

        losses = df[df["profit_loss"] <= 0]

        total_wins = len(wins)

        total_losses = len(losses)

        # ======================================
        # WINRATE
        # ======================================

        winrate = 0

        if total_trades > 0:

            winrate = round((total_wins / total_trades) * 100, 2)

        # ======================================
        # AVG GAIN / LOSS
        # ======================================

        avg_gain = 0

        if not wins.empty:

            avg_gain = round(wins["profit_loss"].mean(), 2)

        avg_loss = 0

        if not losses.empty:

            avg_loss = round(losses["profit_loss"].mean(), 2)

        # ======================================
        # PROFIT FACTOR
        # ======================================

        gross_profit = wins["profit_loss"].sum()

        gross_loss = abs(losses["profit_loss"].sum())

        profit_factor = 0

        if gross_loss > 0:

            profit_factor = round(gross_profit / gross_loss, 2)

        # ======================================
        # EXPECTANCY
        # ======================================

        expectancy = round(
            ((winrate / 100) * avg_gain) + ((1 - (winrate / 100)) * avg_loss), 2
        )

        # ======================================
        # EQUITY CURVE
        # ======================================

        df["equity"] = df["profit_loss"].cumsum()

        # ======================================
        # MAX DRAWDOWN
        # ======================================

        rolling_max = df["equity"].cummax()

        drawdown = df["equity"] - rolling_max

        max_drawdown = round(drawdown.min(), 2)

        # ======================================
        # SHARPE RATIO
        # ======================================

        sharpe_ratio = 0

        if df["profit_loss"].std() != 0:

            sharpe_ratio = round(
                (df["profit_loss"].mean()) / (df["profit_loss"].std()), 2
            )

        return {
            "total_trades": total_trades,
            "winrate": winrate,
            "average_gain": avg_gain,
            "average_loss": avg_loss,
            "profit_factor": (profit_factor),
            "expectancy": expectancy,
            "max_drawdown": (max_drawdown),
            "sharpe_ratio": (sharpe_ratio),
        }

    except Exception as e:

        print(f"❌ Performance analytics error: " f"{e}")

        return {}
