import numpy as np
import pandas as pd

from infrastructure.logger import logger

# ======================================
# PERFORMANCE ANALYTICS ENGINE
# ======================================


def analyze_performance(trades):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if not trades:

            return {}

        df = pd.DataFrame(trades)

        # ======================================
        # REQUIRED COLUMNS
        # ======================================

        required_columns = ["profit_loss"]

        missing = [col for col in required_columns if col not in df.columns]

        if missing:

            logger.warning(f"Missing columns: " f"{missing}")

            return {}

        # ======================================
        # CLEAN DATA
        # ======================================

        df = df.copy()

        df["profit_loss"] = pd.to_numeric(df["profit_loss"], errors="coerce")

        df = df.dropna(subset=["profit_loss"])

        if df.empty:

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
        # GROSS PROFIT / LOSS
        # ======================================

        gross_profit = round(wins["profit_loss"].sum(), 2)

        gross_loss = abs(round(losses["profit_loss"].sum(), 2))

        # ======================================
        # PROFIT FACTOR
        # ======================================

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
        # MAX DRAWDOWN %
        # ======================================

        rolling_max = df["equity"].cummax()

        drawdown = df["equity"] - rolling_max

        max_drawdown = round(drawdown.min(), 2)

        max_drawdown_pct = 0

        if rolling_max.max() != 0:

            max_drawdown_pct = round((abs(drawdown.min()) / rolling_max.max()) * 100, 2)

        # ======================================
        # SHARPE RATIO
        # ======================================

        sharpe_ratio = 0

        pnl_std = df["profit_loss"].std()

        if pnl_std != 0:

            sharpe_ratio = round((df["profit_loss"].mean() / pnl_std) * np.sqrt(252), 2)

        # ======================================
        # WIN / LOSS STREAK
        # ======================================

        streak = 0

        max_win_streak = 0

        max_loss_streak = 0

        for pnl in df["profit_loss"]:

            if pnl > 0:

                if streak >= 0:

                    streak += 1

                else:

                    streak = 1

            else:

                if streak <= 0:

                    streak -= 1

                else:

                    streak = -1

            max_win_streak = max(max_win_streak, streak)

            max_loss_streak = min(max_loss_streak, streak)

        # ======================================
        # RECOVERY FACTOR
        # ======================================

        recovery_factor = 0

        if abs(max_drawdown) > 0:

            recovery_factor = round(gross_profit / abs(max_drawdown), 2)

        # ======================================
        # HEALTH STATUS
        # ======================================

        health_status = "DANGEROUS"

        if winrate >= 55 and profit_factor >= 1.5 and max_drawdown_pct < 15:

            health_status = "HEALTHY"

        elif winrate >= 45 and profit_factor >= 1:

            health_status = "WARNING"

        # ======================================
        # SURVIVABILITY SCORE
        # ======================================

        survivability_score = round(
            (winrate * 0.35)
            + (profit_factor * 20)
            + (max(0, 20 - max_drawdown_pct) * 1.5),
            2,
        )

        survivability_score = min(survivability_score, 100)

        logger.info("Performance analytics complete")

        return {
            "total_trades": (total_trades),
            "total_wins": (total_wins),
            "total_losses": (total_losses),
            "winrate": (winrate),
            "average_gain": (avg_gain),
            "average_loss": (avg_loss),
            "gross_profit": (gross_profit),
            "gross_loss": (gross_loss),
            "profit_factor": (profit_factor),
            "expectancy": (expectancy),
            "max_drawdown": (max_drawdown),
            "max_drawdown_pct": (max_drawdown_pct),
            "sharpe_ratio": (sharpe_ratio),
            "recovery_factor": (recovery_factor),
            "max_win_streak": (max_win_streak),
            "max_loss_streak": abs(max_loss_streak),
            "survivability_score": (survivability_score),
            "health_status": (health_status),
        }

    except Exception as e:

        logger.error(f"Performance analytics " f"error: {e}")

        return {}
