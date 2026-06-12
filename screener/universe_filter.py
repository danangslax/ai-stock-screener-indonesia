import pandas as pd

from core.data_loader import load_stock_data

# ======================================
# FAST UNIVERSE FILTER
# ======================================


def filter_universe(symbols, max_stocks=100):

    try:

        print("🚀 Running Universe Filter")

        results = []

        total = len(symbols)

        # ======================================
        # LOOP STOCKS
        # ======================================

        for i, symbol in enumerate(symbols):

            try:

                print(f"📊 " f"{i+1}/{total} " f"{symbol}")

                # ======================================
                # LOAD DATA
                # ======================================

                df = load_stock_data(symbol)

                if df.empty:

                    continue

                if len(df) < 30:

                    continue

                latest = df.iloc[-1]

                # ======================================
                # BASIC DATA
                # ======================================

                price = float(latest["Close"])

                volume = float(latest["Volume"])

                value = price * volume

                # ======================================
                # BASIC VOLATILITY
                # ======================================

                volatility = df["Close"].pct_change().rolling(20).std().iloc[-1]

                # ======================================
                # FAST FILTERS
                # ======================================

                # Avoid gocap
                if price < 50:

                    continue

                # Avoid expensive
                if price > 10000:

                    continue

                # Minimum liquidity
                if volume < 500_000:

                    continue

                # Minimum transaction value
                if value < 5_000_000_000:

                    continue

                # Avoid crazy volatility
                if volatility > 0.20:

                    continue

                # ======================================
                # SAVE
                # ======================================

                results.append(
                    {
                        "symbol": symbol,
                        "price": price,
                        "volume": volume,
                        "value": value,
                        "volatility": volatility,
                    }
                )

            except Exception as e:

                print(f"❌ Universe Error " f"{symbol}: {e}")

        # ======================================
        # DATAFRAME
        # ======================================

        result_df = pd.DataFrame(results)

        if result_df.empty:

            return []

        # ======================================
        # SORT LIQUIDITY
        # ======================================

        result_df = result_df.sort_values(by="value", ascending=False).reset_index(
            drop=True
        )

        # ======================================
        # TOP STOCKS
        # ======================================

        filtered_symbols = result_df["symbol"].head(max_stocks).tolist()

        print("")

        print("=================================")

        print(f"✅ Universe Filter Complete")

        print(f"Input: {len(symbols)}")

        print(f"Output: " f"{len(filtered_symbols)}")

        print("=================================")

        return filtered_symbols

    except Exception as e:

        print(f"❌ Universe Filter Error: " f"{e}")

        return []
