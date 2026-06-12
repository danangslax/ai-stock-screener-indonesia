import pandas as pd

from core.data_loader import load_stock_data

from storage.indicators import add_indicators

from core.relative_strength import calculate_relative_strength

# ======================================
# ANALYZE MARKET BREADTH
# ======================================


def analyze_market_breadth(symbols):

    try:

        # ======================================
        # COUNTERS
        # ======================================

        total = 0

        above_ma20 = 0

        bullish_rsi = 0

        breakout_count = 0

        strong_rs = 0

        # ======================================
        # LOOP SYMBOLS
        # ======================================

        for symbol in symbols:

            try:

                # ======================================
                # LOAD DATA
                # ======================================

                df = load_stock_data(symbol, period="6mo", interval="1d")

                if df.empty:

                    continue

                if len(df) < 50:

                    continue

                # ======================================
                # INDICATORS
                # ======================================

                df = add_indicators(df)

                if df.empty:

                    continue

                latest = df.iloc[-1]

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

                print(f"BREADTH ERROR " f"{symbol}: {e}")

        # ======================================
        # VALIDATION
        # ======================================

        if total == 0:

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
        # RETURN RESULT
        # ======================================

        return {
            "total_stocks": total,
            "above_ma20_pct": (above_ma20_pct),
            "bullish_rsi_pct": (bullish_rsi_pct),
            "breakout_pct": (breakout_pct),
            "strong_rs_pct": (strong_rs_pct),
            "health_score": (health_score),
            "status": status,
        }

    except Exception as e:

        print(f"MARKET BREADTH ERROR: " f"{e}")

        return None
