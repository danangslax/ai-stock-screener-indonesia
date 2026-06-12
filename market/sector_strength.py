import pandas as pd

from collections import defaultdict

from core.data_loader import load_stock_data

from core.relative_strength import calculate_relative_strength

from watchlist.sectors import SECTOR_MAP

# ======================================
# ANALYZE SECTOR STRENGTH
# ======================================


def analyze_sector_strength():

    try:

        # ======================================
        # SECTOR CONTAINER
        # ======================================

        sector_data = defaultdict(list)

        # ======================================
        # LOOP STOCKS
        # ======================================

        for symbol, sector in SECTOR_MAP.items():

            try:

                # ======================================
                # LOAD DATA
                # ======================================

                df = load_stock_data(symbol, period="6mo", interval="1d")

                if df.empty:

                    continue

                if len(df) < 30:

                    continue

                # ======================================
                # RETURN
                # ======================================

                stock_return = round(
                    (df["Close"].iloc[-1] / df["Close"].iloc[-20] - 1) * 100, 2
                )

                # ======================================
                # RSI
                # ======================================

                delta = df["Close"].diff()

                gain = delta.where(delta > 0, 0).rolling(14).mean()

                loss = -delta.where(delta < 0, 0).rolling(14).mean()

                rs = gain / loss

                rsi = round((100 - (100 / (1 + rs))).iloc[-1], 2)

                # ======================================
                # RELATIVE STRENGTH
                # ======================================

                rs_analysis = calculate_relative_strength(df)

                if rs_analysis is None:

                    continue

                rs_ratio = rs_analysis["rs_ratio"]

                # ======================================
                # BULLISH
                # ======================================

                bullish = stock_return > 0 and rsi > 50

                # ======================================
                # SAVE
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

                print(f"SECTOR ERROR " f"{symbol}: {e}")

        # ======================================
        # RESULT
        # ======================================

        results = []

        # ======================================
        # ANALYZE EACH SECTOR
        # ======================================

        for sector, stocks in sector_data.items():

            if not stocks:

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

            score = 0

            # Return
            score += avg_return * 2

            # RSI
            score += avg_rsi * 0.5

            # Relative Strength
            score += avg_rs * 20

            # Bullish Breadth
            score += bullish_percent * 0.3

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
                    "Score": round(score, 2),
                    "Average_Return": (avg_return),
                    "Average_RSI": (avg_rsi),
                    "Average_RS": (avg_rs),
                    "Bullish_%": (bullish_percent),
                    "Leader": leader,
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

        return result_df

    except Exception as e:

        print(f"SECTOR STRENGTH ERROR: " f"{e}")

        return pd.DataFrame()
