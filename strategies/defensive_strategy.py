# ======================================
# DEFENSIVE STRATEGY
# ======================================


def defensive_strategy(latest, df):

    try:

        volatility = float(latest["VOLATILITY"])

        rsi = float(latest["RSI"])

        ema20 = float(latest["EMA20"])

        ema50 = float(latest["EMA50"])

        relative_volume = latest["Volume"] / latest["VOL_MA20"]

        # ======================================
        # CONDITIONS
        # ======================================

        conditions = [
            # low volatility
            volatility < 0.08,
            # stable RSI
            50 <= rsi <= 70,
            # trend stability
            ema20 > ema50,
            # decent volume
            relative_volume >= 1,
        ]

        score = sum(conditions) * 25

        status = "PASS" if score >= 75 else "FAIL"

        return {"strategy": "DEFENSIVE", "status": status, "score": score}

    except Exception as e:

        print(f"❌ Defensive strategy error: " f"{e}")

        return None
