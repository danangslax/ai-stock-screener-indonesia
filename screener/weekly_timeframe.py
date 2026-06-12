# ======================================
# WEEKLY TIMEFRAME ANALYSIS
# ======================================


def analyze_weekly_timeframe(df):

    try:

        if df.empty:

            return None

        latest = df.iloc[-1]

        # ======================================
        # INDICATORS
        # ======================================

        close = float(latest["Close"])

        ema20 = float(latest["EMA20"])

        ema50 = float(latest["EMA50"])

        rsi = float(latest["RSI"])

        adx = float(latest["ADX"])

        volatility = float(latest["VOLATILITY"])

        # ======================================
        # CONDITIONS
        # ======================================

        conditions = [
            # major trend
            close > ema20,
            # long trend
            ema20 > ema50,
            # healthy momentum
            rsi >= 50,
            # trend strength
            adx >= 20,
            # acceptable volatility
            volatility < 0.15,
        ]

        score = sum(conditions) * 20

        # ======================================
        # STATUS
        # ======================================

        if score >= 80:

            status = "STRONG"

        elif score >= 60:

            status = "GOOD"

        else:

            status = "WEAK"

        return {"status": status, "score": score}

    except Exception as e:

        print(f"❌ Weekly analysis error: " f"{e}")

        return None
