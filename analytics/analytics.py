import numpy as np
import pandas as pd

from infrastructure.logger import logger

# ======================================
# DEFAULT METRICS
# ======================================

DEFAULT_METRICS = {
    "total_trades": 0,
    "open_trades": 0,
    "closed_trades": 0,
    "winning_trades": 0,
    "losing_trades": 0,
    "winrate": 0,
    "total_pnl": 0,
    "average_pnl": 0,
    "best_trade": 0,
    "worst_trade": 0,
    "average_rr": 0,
    "profit_factor": 0,
    "expectancy": 0,
    "max_drawdown": 0,
    "max_drawdown_pct": 0,
    "sharpe_ratio": 0,
    "health_status": "UNKNOWN",
    "survivability_score": 0,
}

# ======================================
# PORTFOLIO ANALYTICS
# ======================================


def calculate_portfolio_metrics(trades):

    try:

        # ======================================
        # EMPTY VALIDATION
        # ======================================

        if not trades:

            return DEFAULT_METRICS.copy()

        # ======================================
        # DATAFRAME
        # ======================================

        df = pd.DataFrame(trades)

        if df.empty:

            return DEFAULT_METRICS.copy()

        # ======================================
        # REQUIRED COLUMNS
        # ======================================

        required_columns = ["status", "profit_loss"]

        missing = [col for col in required_columns if col not in df.columns]

        if missing:

            logger.warning(f"Missing columns: " f"{missing}")

            return DEFAULT_METRICS.copy()

        # ======================================
        # CLEAN DATA
        # ======================================

        df = df.copy()

        df["profit_loss"] = pd.to_numeric(df["profit_loss"], errors="coerce").fillna(0)

        # ======================================
        # TOTAL TRADES
        # ======================================

        total_trades = len(df)

        open_trades = len(df[df["status"] == "OPEN"])

        closed_df = df[df["status"] == "CLOSED"].copy()

        closed_trades = len(closed_df)

        # ======================================
        # NO CLOSED TRADES
        # ======================================

        if closed_df.empty:

            result = DEFAULT_METRICS.copy()

            result.update(
                {
                    "total_trades": (total_trades),
                    "open_trades": (open_trades),
                }
            )

            return result

        # ======================================
        # PNL METRICS
        # ======================================

        total_pnl = round(closed_df["profit_loss"].sum(), 2)

        average_pnl = round(closed_df["profit_loss"].mean(), 2)

        best_trade = round(closed_df["profit_loss"].max(), 2)

        worst_trade = round(closed_df["profit_loss"].min(), 2)

        # ======================================
        # WIN / LOSS
        # ======================================

        winning_trades = len(closed_df[closed_df["profit_loss"] > 0])

        losing_trades = len(closed_df[closed_df["profit_loss"] <= 0])

        # ======================================
        # WINRATE
        # ======================================

        winrate = round((winning_trades / closed_trades) * 100, 2)

        # ======================================
        # PROFIT FACTOR
        # ======================================

        gross_profit = closed_df[closed_df["profit_loss"] > 0]["profit_loss"].sum()

        gross_loss = abs(closed_df[closed_df["profit_loss"] < 0]["profit_loss"].sum())

        profit_factor = 0

        if gross_loss > 0:

            profit_factor = round(gross_profit / gross_loss, 2)

        # ======================================
        # EXPECTANCY
        # ======================================

        expectancy = round(total_pnl / closed_trades, 2)

        # ======================================
        # RISK REWARD
        # ======================================

        average_rr = 0

        if "risk_reward" in closed_df.columns:

            rr_series = pd.to_numeric(closed_df["risk_reward"], errors="coerce")

            if not rr_series.empty:

                average_rr = round(rr_series.mean(), 2)

        # ======================================
        # EQUITY CURVE
        # ======================================

        closed_df["equity"] = closed_df["profit_loss"].cumsum()

        # ======================================
        # MAX DRAWDOWN
        # ======================================

        rolling_max = closed_df["equity"].cummax()

        drawdown = closed_df["equity"] - rolling_max

        max_drawdown = round(drawdown.min(), 2)

        max_drawdown_pct = 0

        if rolling_max.max() != 0:

            max_drawdown_pct = round((abs(drawdown.min()) / rolling_max.max()) * 100, 2)

        # ======================================
        # SHARPE RATIO
        # ======================================

        sharpe_ratio = 0

        pnl_std = closed_df["profit_loss"].std()

        if pnl_std != 0:

            sharpe_ratio = round(
                (closed_df["profit_loss"].mean() / pnl_std) * np.sqrt(252), 2
            )

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

        logger.info("Portfolio analytics complete")

        # ======================================
        # RETURN RESULT
        # ======================================

        return {
            "total_trades": (total_trades),
            "open_trades": (open_trades),
            "closed_trades": (closed_trades),
            "winning_trades": (winning_trades),
            "losing_trades": (losing_trades),
            "winrate": (winrate),
            "total_pnl": (total_pnl),
            "average_pnl": (average_pnl),
            "best_trade": (best_trade),
            "worst_trade": (worst_trade),
            "average_rr": (average_rr),
            "profit_factor": (profit_factor),
            "expectancy": (expectancy),
            "max_drawdown": (max_drawdown),
            "max_drawdown_pct": (max_drawdown_pct),
            "sharpe_ratio": (sharpe_ratio),
            "health_status": (health_status),
            "survivability_score": (survivability_score),
        }

    except Exception as e:

        logger.error(f"Portfolio analytics " f"error: {e}")

        return DEFAULT_METRICS.copy()


# ======================================
# EQUITY CURVE
# ======================================


def generate_equity_curve(trades, starting_balance=100_000_000):

    try:

        if not trades:

            return pd.DataFrame()

        df = pd.DataFrame(trades)

        if df.empty:

            return pd.DataFrame()

        # ======================================
        # CLOSED TRADES
        # ======================================

        closed_df = df[df["status"] == "CLOSED"].copy()

        if closed_df.empty:

            return pd.DataFrame()

        # ======================================
        # SORT DATE
        # ======================================

        if "created_at" in closed_df.columns:

            closed_df = closed_df.sort_values(by="created_at")

        # ======================================
        # CLEAN PNL
        # ======================================

        closed_df["profit_loss"] = pd.to_numeric(
            closed_df["profit_loss"], errors="coerce"
        ).fillna(0)

        # ======================================
        # EQUITY
        # ======================================

        equity = []

        current_balance = starting_balance

        # ======================================
        # BUILD CURVE
        # ======================================

        for pnl in closed_df["profit_loss"]:

            current_balance += pnl

            equity.append(current_balance)

        closed_df["equity"] = equity

        # ======================================
        # RETURN %
        # ======================================

        closed_df["return_pct"] = round(
            ((closed_df["equity"] - starting_balance) / starting_balance) * 100, 2
        )

        # ======================================
        # EQUITY PEAK
        # ======================================

        closed_df["equity_peak"] = closed_df["equity"].cummax()

        # ======================================
        # DRAWDOWN %
        # ======================================

        closed_df["drawdown_pct"] = round(
            (
                (closed_df["equity"] - closed_df["equity_peak"])
                / closed_df["equity_peak"]
            )
            * 100,
            2,
        )

        logger.info("Equity curve generated")

        return closed_df

    except Exception as e:

        logger.error(f"Equity curve error: " f"{e}")

        return pd.DataFrame()
