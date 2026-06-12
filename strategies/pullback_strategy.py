# ======================================
# PULLBACK STRATEGY
# ======================================


def pullback_strategy(latest, df):

    try:

        price = float(latest["Close"])

        ma20 = float(latest["MA20"])

        ema20 = float(latest["EMA20"])

        ema50 = float(latest["EMA50"])

        rsi = float(latest["RSI"])

        adx = float(latest["ADX"])

        volatility = float(latest["VOLATILITY"])

        # ======================================
        # DISTANCE FROM MA20
        # ======================================

        distance_ma20 = abs((price - ma20) / ma20)

        # ======================================
        # CONDITIONS
        # ======================================

        conditions = [
            # healthy trend
            ema20 > ema50,
            # near MA20 pullback
            distance_ma20 <= 0.03,
            # healthy RSI
            50 <= rsi <= 65,
            # trend strength
            adx >= 20,
            # controlled volatility
            volatility < 0.12,
        ]

        score = sum(conditions) * 20

        status = "PASS" if score >= 80 else "FAIL"

        return {"strategy": "PULLBACK", "status": status, "score": score}

    except Exception as e:

        print(f"❌ Pullback strategy error: " f"{e}")

        return None
