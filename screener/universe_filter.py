import pandas as pd

from infrastructure.logger import logger

from storage.data_loader import load_stock_data

# ======================================
# FAST UNIVERSE FILTER
# ======================================


def filter_universe(symbols, max_stocks=100):

    try:

        logger.info("Running Universe Filter")

        results = []

        total = len(symbols)

        # ======================================
        # FILTER STATISTICS
        # ======================================

        skipped_price = 0

        skipped_liquidity = 0

        skipped_value = 0

        skipped_volatility = 0

        skipped_invalid = 0

        # ======================================
        # LOOP STOCKS
        # ======================================

        for i, symbol in enumerate(symbols):

            try:

                logger.info(f"Universe Filter " f"{i+1}/{total} " f"{symbol}")

                # ======================================
                # LOAD CACHE DATA
                # ======================================

                df = load_stock_data(symbol, use_cache=True, cache_only=True)

                # ======================================
                # VALIDATION
                # ======================================

                if df.empty:

                    skipped_invalid += 1

                    continue

                if len(df) < 30:

                    skipped_invalid += 1

                    continue

                latest = df.iloc[-1]

                # ======================================
                # REQUIRED COLUMNS
                # ======================================

                required_columns = ["Close", "Volume", "VOLATILITY", "VOL_MA20"]

                missing = [col for col in required_columns if col not in latest]

                if missing:

                    skipped_invalid += 1

                    continue

                # ======================================
                # BASIC DATA
                # ======================================

                price = float(latest["Close"])

                volume = float(latest["Volume"])

                avg_volume = float(latest["VOL_MA20"])

                volatility = float(latest["VOLATILITY"])

                # ======================================
                # NAN VALIDATION
                # ======================================

                metrics = [price, volume, avg_volume, volatility]

                if any(pd.isna(v) for v in metrics):

                    skipped_invalid += 1

                    continue

                # ======================================
                # LIQUIDITY VALUE
                # ======================================

                transaction_value = price * avg_volume

                # ======================================
                # PRICE FILTER
                # ======================================

                if price < 50:

                    skipped_price += 1

                    continue

                if price > 10000:

                    skipped_price += 1

                    continue

                # ======================================
                # LIQUIDITY FILTER
                # ======================================

                if avg_volume < 500_000:

                    skipped_liquidity += 1

                    continue

                # ======================================
                # TRANSACTION VALUE
                # ======================================

                if transaction_value < 5_000_000_000:

                    skipped_value += 1

                    continue

                # ======================================
                # VOLATILITY FILTER
                # ======================================

                if volatility > 0.20:

                    skipped_volatility += 1

                    continue

                # ======================================
                # SAVE RESULT
                # ======================================

                results.append(
                    {
                        "symbol": symbol,
                        "price": round(price, 2),
                        "avg_volume": int(avg_volume),
                        "transaction_value": int(transaction_value),
                        "volatility": round(volatility, 4),
                    }
                )

            except Exception as e:

                logger.error(f"Universe Error " f"{symbol}: {e}")

        # ======================================
        # DATAFRAME
        # ======================================

        result_df = pd.DataFrame(results)

        if result_df.empty:

            logger.warning("Universe filter returned empty")

            return []

        # ======================================
        # SORT LIQUIDITY
        # ======================================

        result_df = result_df.sort_values(
            by="transaction_value", ascending=False
        ).reset_index(drop=True)

        # ======================================
        # TOP STOCKS
        # ======================================

        filtered_symbols = result_df["symbol"].head(max_stocks).tolist()

        # ======================================
        # SUMMARY
        # ======================================

        logger.info("=================================")

        logger.info("Universe Filter Complete")

        logger.info(f"Input Stocks: " f"{len(symbols)}")

        logger.info(f"Filtered Stocks: " f"{len(filtered_symbols)}")

        logger.info(f"Skipped Price: " f"{skipped_price}")

        logger.info(f"Skipped Liquidity: " f"{skipped_liquidity}")

        logger.info(f"Skipped Value: " f"{skipped_value}")

        logger.info(f"Skipped Volatility: " f"{skipped_volatility}")

        logger.info(f"Skipped Invalid: " f"{skipped_invalid}")

        logger.info("=================================")

        return filtered_symbols

    except Exception as e:

        logger.error(f"Universe Filter Error: {e}")

        return []
