import pandas as pd

from infrastructure.logger import logger

# ======================================
# STRATEGY PERFORMANCE ANALYTICS
# ======================================


def analyze_strategy_performance(trades):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if not trades:

            return pd.DataFrame()

        df = pd.DataFrame(trades)

        if df.empty:

            return pd.DataFrame()

        # ======================================
        # REQUIRED COLUMNS
        # ======================================

        required_columns = ["strategy", "profit_loss"]

        missing = [col for col in required_columns if col not in df.columns]

        if missing:

            logger.warning(f"Missing columns: " f"{missing}")

            return pd.DataFrame()

        # ======================================
        # CLEAN DATA
        # ======================================

        df = df.copy()

        df["profit_loss"] = pd.to_numeric(df["profit_loss"], errors="coerce").fillna(0)

        # ======================================
        # GROUP STRATEGIES
        # ======================================

        results = []

        strategies = sorted(df["strategy"].dropna().unique())

        # ======================================
        # LOOP STRATEGIES
        # ======================================

        for strategy in strategies:

            try:

                strategy_df = df[df["strategy"] == strategy].copy()

                if strategy_df.empty:

                    continue

                # ======================================
                # BASIC STATS
                # ======================================

                total_trades = len(strategy_df)

                total_pnl = round(strategy_df["profit_loss"].sum(), 2)

                average_pnl = round(strategy_df["profit_loss"].mean(), 2)

                best_trade = round(strategy_df["profit_loss"].max(), 2)

                worst_trade = round(strategy_df["profit_loss"].min(), 2)

                # ======================================
                # WIN / LOSS
                # ======================================

                wins = strategy_df[strategy_df["profit_loss"] > 0]

                losses = strategy_df[strategy_df["profit_loss"] <= 0]

                total_wins = len(wins)

                total_losses = len(losses)

                # ======================================
                # WINRATE
                # ======================================

                winrate = round((total_wins / total_trades) * 100, 2)

                # ======================================
                # PROFIT FACTOR
                # ======================================

                gross_profit = round(wins["profit_loss"].sum(), 2)

                gross_loss = abs(round(losses["profit_loss"].sum(), 2))

                profit_factor = 0

                if gross_loss > 0:

                    profit_factor = round(gross_profit / gross_loss, 2)

                # ======================================
                # EXPECTANCY
                # ======================================

                expectancy = round(average_pnl, 2)

                # ======================================
                # MAX DRAWDOWN
                # ======================================

                strategy_df["equity"] = strategy_df["profit_loss"].cumsum()

                rolling_max = strategy_df["equity"].cummax()

                drawdown = strategy_df["equity"] - rolling_max

                max_drawdown = round(drawdown.min(), 2)

                # ======================================
                # CONFIDENCE
                # ======================================

                avg_confidence = 0

                if "confidence" in strategy_df.columns:

                    avg_confidence = round(
                        pd.to_numeric(
                            strategy_df["confidence"], errors="coerce"
                        ).mean(),
                        2,
                    )

                # ======================================
                # MARKET REGIMES
                # ======================================

                best_regime = "UNKNOWN"

                if "market_regime" in strategy_df.columns:

                    regime_analysis = strategy_df.groupby("market_regime")[
                        "profit_loss"
                    ].mean()

                    if not regime_analysis.empty:

                        best_regime = regime_analysis.idxmax()

                # ======================================
                # HEALTH STATUS
                # ======================================

                status = "WEAK"

                if winrate >= 60 and profit_factor >= 1.5:

                    status = "ROBUST"

                elif winrate >= 50 and profit_factor >= 1:

                    status = "STABLE"

                # ======================================
                # SURVIVABILITY SCORE
                # ======================================

                survivability_score = round(
                    (winrate * 0.4)
                    + (profit_factor * 20)
                    + (max(0, 20 - abs(max_drawdown)) * 1.2),
                    2,
                )

                survivability_score = min(survivability_score, 100)

                # ======================================
                # AI RANK SCORE
                # ======================================

                ai_rank_score = round(
                    (winrate * 0.35)
                    + (profit_factor * 25)
                    + (avg_confidence * 0.2)
                    + (survivability_score * 0.2),
                    2,
                )

                # ======================================
                # SAVE RESULT
                # ======================================

                results.append(
                    {
                        "Strategy": (strategy),
                        "Total_Trades": (total_trades),
                        "Winning_Trades": (total_wins),
                        "Losing_Trades": (total_losses),
                        "Winrate": (winrate),
                        "Total_PnL": (total_pnl),
                        "Average_PnL": (average_pnl),
                        "Best_Trade": (best_trade),
                        "Worst_Trade": (worst_trade),
                        "Profit_Factor": (profit_factor),
                        "Expectancy": (expectancy),
                        "Max_Drawdown": (max_drawdown),
                        "Average_Confidence": (avg_confidence),
                        "Best_Regime": (best_regime),
                        "Survivability_Score": (survivability_score),
                        "AI_Rank_Score": (ai_rank_score),
                        "Status": (status),
                    }
                )

            except Exception as strategy_error:

                logger.error(f"Strategy analysis " f"error: " f"{strategy_error}")

        # ======================================
        # DATAFRAME
        # ======================================

        result_df = pd.DataFrame(results)

        if result_df.empty:

            return pd.DataFrame()

        # ======================================
        # SORT
        # ======================================

        result_df = result_df.sort_values(
            by="AI_Rank_Score", ascending=False
        ).reset_index(drop=True)

        logger.info("Strategy analytics complete")

        return result_df

    except Exception as e:

        logger.error(f"Strategy analytics " f"error: {e}")

        return pd.DataFrame()
