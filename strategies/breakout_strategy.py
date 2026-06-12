# ======================================
# BREAKOUT STRATEGY
# ======================================


def breakout_strategy(latest, df):

    try:

        price = float(latest["Close"])

        volume = float(latest["Volume"])

        ma20 = float(latest["MA20"])

        rsi = float(latest["RSI"])

        adx = float(latest["ADX"])

        vol_ma20 = float(latest["VOL_MA20"])

        high_20 = float(latest["HIGH_20"])

        # ======================================
        # CONDITIONS
        # ======================================

        conditions = [
            # breakout
            price >= high_20 * 0.98,
            # strong trend
            adx >= 25,
            # healthy RSI
            55 <= rsi <= 80,
            # volume expansion
            volume > (1.5 * vol_ma20),
            # trend alignment
            price > ma20,
        ]

        score = sum(conditions) * 20

        status = "PASS" if score >= 80 else "FAIL"

        return {"strategy": "BREAKOUT", "status": status, "score": score}

    except Exception as e:

        print(f"❌ Breakout strategy error: " f"{e}")

        return None
