import pandas as pd

from infrastructure.logger import logger

from storage.data_loader import load_stock_data

from screener.relative_strength import calculate_relative_strength

# ======================================
# ANALYZE MARKET BREADTH
# ======================================


def analyze_market_breadth(symbols, max_symbols=200):

    try:

        logger.info("Analyzing market breadth")

        # ======================================
        # LIMIT SYMBOLS
        # ======================================

        symbols = symbols[:max_symbols]

        # ======================================
        # COUNTERS
        # ======================================

        total = 0

        above_ma20 = 0

        bullish_rsi = 0

        breakout_count = 0

        strong_rs = 0

        skipped = 0

        # ======================================
        # LOOP SYMBOLS
        # ======================================

        for i, symbol in enumerate(symbols):

            try:

                logger.info(f"Breadth " f"{i+1}/{len(symbols)} " f"{symbol}")

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

                if len(df) < 50:

                    skipped += 1

                    continue

                latest = df.iloc[-1]

                # ======================================
                # REQUIRED METRICS
                # ======================================

                required_metrics = ["Close", "MA20", "RSI", "High"]

                missing = [col for col in required_metrics if col not in df.columns]

                if missing:

                    skipped += 1

                    logger.warning(f"Missing columns " f"{symbol}: " f"{missing}")

                    continue

                total += 1

                # ======================================
                # ABOVE MA20
                # ======================================

                if latest["Close"] > latest["MA20"]:

                    above_ma20 += 1

                # ======================================
                # BULLISH RSI
                # ======================================

                if latest["RSI"] >= 50:

                    bullish_rsi += 1

                # ======================================
                # BREAKOUT
                # ======================================

                highest_20 = df["High"].rolling(20).max().iloc[-2]

                if latest["Close"] >= highest_20:

                    breakout_count += 1

                # ======================================
                # RELATIVE STRENGTH
                # ======================================

                rs_analysis = calculate_relative_strength(df)

                if rs_analysis:

                    if rs_analysis["status"] in ["MARKET LEADER", "STRONG"]:

                        strong_rs += 1

            except Exception as e:

                skipped += 1

                logger.warning(f"Breadth Error " f"{symbol}: {e}")

        # ======================================
        # VALIDATION
        # ======================================

        if total == 0:

            logger.warning("No valid breadth data")

            return None

        # ======================================
        # PERCENTAGES
        # ======================================

        above_ma20_pct = round((above_ma20 / total) * 100, 2)

        bullish_rsi_pct = round((bullish_rsi / total) * 100, 2)

        breakout_pct = round((breakout_count / total) * 100, 2)

        strong_rs_pct = round((strong_rs / total) * 100, 2)

        # ======================================
        # HEALTH SCORE
        # ======================================

        health_score = round(
            (above_ma20_pct * 0.35)
            + (bullish_rsi_pct * 0.25)
            + (breakout_pct * 0.20)
            + (strong_rs_pct * 0.20),
            2,
        )

        # ======================================
        # STATUS
        # ======================================

        if health_score >= 75:

            status = "STRONG BULL MARKET"

        elif health_score >= 60:

            status = "BULLISH"

        elif health_score >= 40:

            status = "NEUTRAL"

        else:

            status = "WEAK MARKET"

        # ======================================
        # RESULT
        # ======================================

        result = {
            "total_stocks": total,
            "skipped_stocks": skipped,
            "above_ma20_pct": (above_ma20_pct),
            "bullish_rsi_pct": (bullish_rsi_pct),
            "breakout_pct": (breakout_pct),
            "strong_rs_pct": (strong_rs_pct),
            "health_score": (health_score),
            "status": status,
        }

        logger.info(f"Market Breadth: " f"{status} | " f"Score={health_score}")

        return result

    except Exception as e:

        logger.error(f"Market Breadth Error: " f"{e}")

        return None
