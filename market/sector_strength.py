import pandas as pd

from collections import defaultdict

from infrastructure.logger import logger

from storage.data_loader import load_stock_data

from storage.indicators import add_indicators

from screener.relative_strength import calculate_relative_strength

from watchlist.sectors import SECTOR_MAP

# ======================================
# ANALYZE SECTOR STRENGTH
# ======================================


def analyze_sector_strength():

    try:

        logger.info("Analyzing sector strength")

        # ======================================
        # SECTOR CONTAINER
        # ======================================

        sector_data = defaultdict(list)

        skipped = 0

        # ======================================
        # LOOP STOCKS
        # ======================================

        total_symbols = len(SECTOR_MAP)

        for i, (symbol, sector) in enumerate(SECTOR_MAP.items()):

            try:

                logger.info(f"Sector " f"{i+1}/{total_symbols} " f"{symbol}")

                # ======================================
                # LOAD DATA
                # ======================================

                df = load_stock_data(
                    symbol, period="6mo", interval="1d", use_cache=True
                )

                # ======================================
                # VALIDATION
                # ======================================

                if df.empty:

                    skipped += 1

                    continue

                if len(df) < 60:

                    skipped += 1

                    continue

                # ======================================
                # ADD INDICATORS
                # ======================================

                df = add_indicators(df)

                if df.empty:

                    skipped += 1

                    continue

                latest = df.iloc[-1]

                # ======================================
                # BASIC METRICS
                # ======================================

                stock_return = round(
                    (df["Close"].iloc[-1] / df["Close"].iloc[-20] - 1) * 100, 2
                )

                rsi = round(float(latest["RSI"]), 2)

                # ======================================
                # RELATIVE STRENGTH
                # ======================================

                rs_analysis = calculate_relative_strength(df)

                if rs_analysis is None:

                    skipped += 1

                    continue

                rs_ratio = round(rs_analysis["rs_ratio"], 2)

                # ======================================
                # NAN VALIDATION
                # ======================================

                metrics = [stock_return, rsi, rs_ratio]

                if any(pd.isna(v) for v in metrics):

                    skipped += 1

                    continue

                # ======================================
                # BULLISH STATUS
                # ======================================

                bullish = stock_return > 0 and rsi > 50

                # ======================================
                # SAVE DATA
                # ======================================

                sector_data[sector].append(
                    {
                        "symbol": symbol,
                        "return": stock_return,
                        "rsi": rsi,
                        "rs_ratio": rs_ratio,
                        "bullish": bullish,
                    }
                )

            except Exception as e:

                skipped += 1

                logger.warning(f"Sector Error " f"{symbol}: {e}")

        # ======================================
        # RESULTS
        # ======================================

        results = []

        # ======================================
        # ANALYZE SECTORS
        # ======================================

        for sector, stocks in sector_data.items():

            # ======================================
            # MINIMUM MEMBERS
            # ======================================

            if len(stocks) < 2:

                continue

            sector_df = pd.DataFrame(stocks)

            # ======================================
            # METRICS
            # ======================================

            avg_return = round(sector_df["return"].mean(), 2)

            avg_rsi = round(sector_df["rsi"].mean(), 2)

            avg_rs = round(sector_df["rs_ratio"].mean(), 2)

            bullish_percent = round(
                (sector_df["bullish"].sum() / len(sector_df)) * 100, 2
            )

            # ======================================
            # SECTOR SCORE
            # ======================================

            score = round(
                (avg_return * 1.5)
                + (avg_rsi * 0.4)
                + (avg_rs * 15)
                + (bullish_percent * 0.25),
                2,
            )

            # ======================================
            # LEADER
            # ======================================

            leader = sector_df.sort_values(by="rs_ratio", ascending=False).iloc[0][
                "symbol"
            ]

            # ======================================
            # STATUS
            # ======================================

            if score >= 120:

                status = "SUPER STRONG"

            elif score >= 90:

                status = "STRONG"

            elif score >= 60:

                status = "NEUTRAL"

            else:

                status = "WEAK"

            # ======================================
            # SAVE RESULT
            # ======================================

            results.append(
                {
                    "Sector": sector,
                    "Score": score,
                    "Average_Return": (avg_return),
                    "Average_RSI": (avg_rsi),
                    "Average_RS": (avg_rs),
                    "Bullish_%": (bullish_percent),
                    "Leader": leader,
                    "Members": len(sector_df),
                    "Status": status,
                }
            )

        # ======================================
        # DATAFRAME
        # ======================================

        result_df = pd.DataFrame(results)

        # ======================================
        # SORT
        # ======================================

        if not result_df.empty:

            result_df = result_df.sort_values(by="Score", ascending=False).reset_index(
                drop=True
            )

        logger.info("Sector strength completed")

        return result_df

    except Exception as e:

        logger.error(f"Sector Strength " f"Error: {e}")

        return pd.DataFrame()
