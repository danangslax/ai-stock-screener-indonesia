# ======================================
# AI SCORING SYSTEM
# ======================================


def calculate_score(row, df):

    try:

        score = 0

        # =================================
        # TREND STRUCTURE
        # =================================

        # Price above MA5
        if row["Close"] > row["MA5"]:
            score += 10

        # Price above MA20
        if row["Close"] > row["MA20"]:
            score += 15

        # Price above MA50
        if row["Close"] > row["MA50"]:
            score += 10

        # Price above EMA20
        if row["Close"] > row["EMA20"]:
            score += 10

        # EMA20 above EMA50
        if row["EMA20"] > row["EMA50"]:
            score += 15

        # MA5 above MA20
        if row["MA5"] > row["MA20"]:
            score += 10

        # =================================
        # RSI MOMENTUM
        # =================================

        # Bullish momentum
        if row["RSI"] >= 50:
            score += 10

        # Strong momentum
        if row["RSI"] >= 60:
            score += 10

        # Sweet spot
        if 65 <= row["RSI"] <= 75:
            score += 5

        # Overbought
        if row["RSI"] >= 80:
            score -= 15

        # Weak RSI
        if row["RSI"] < 45:
            score -= 10

        # =================================
        # MACD MOMENTUM
        # =================================

        # MACD bullish crossover
        if row["MACD"] > row["MACD_SIGNAL"]:
            score += 10

        # Positive histogram
        if row["MACD_HIST"] > 0:
            score += 5

        # =================================
        # VOLUME ANALYSIS
        # =================================

        # Above average volume
        if row["Volume"] > row["VOL_MA20"]:
            score += 10

        # Strong volume breakout
        if row["Volume"] > (1.5 * row["VOL_MA20"]):
            score += 15

        # Extreme volume spike
        if row["Volume"] > (2.5 * row["VOL_MA20"]):
            score += 5

        # =================================
        # BOLLINGER ANALYSIS
        # =================================

        # Above BB middle
        if row["Close"] > row["BB_MIDDLE"]:
            score += 5

        # Breakout above upper band
        if row["Close"] > row["BB_UPPER"]:
            score += 10

        # Bollinger expansion
        if row["BB_WIDTH"] > (row["Close"] * 0.05):
            score += 5

        # =================================
        # BREAKOUT DETECTION
        # =================================

        # 20-day breakout
        if row["Close"] >= row["HIGH_20"]:
            score += 20

        # =================================
        # ADX TREND STRENGTH
        # =================================

        # Healthy trend
        if row["ADX"] >= 20:
            score += 5

        # Strong trend
        if row["ADX"] >= 25:
            score += 10

        # Very strong trend
        if row["ADX"] >= 35:
            score += 5

        # =================================
        # MOMENTUM FILTER
        # =================================

        weekly_return = row["WEEKLY_RETURN"]

        monthly_return = row["MONTHLY_RETURN"]

        # Sweet spot momentum
        if weekly_return >= 0.05 and weekly_return <= 0.30:
            score += 10

        # Strong monthly trend
        if monthly_return > 0:
            score += 5

        # Too extended
        if weekly_return > 0.30:
            score -= 10

        # =================================
        # VOLATILITY FILTER
        # =================================

        volatility = row["VOLATILITY"]

        # Stable trend
        if volatility < 0.05:
            score += 5

        # Too volatile
        if volatility > 0.12:
            score -= 10

        # =================================
        # ATR FILTER
        # =================================

        atr_percent = row["ATR"] / row["Close"]

        # Healthy volatility
        if 0.02 <= atr_percent <= 0.08:
            score += 5

        # Too risky
        if atr_percent > 0.10:
            score -= 10

        # =================================
        # DISTANCE FROM MA20
        # =================================

        # Not too extended
        if abs(row["DISTANCE_MA20"]) <= 15:
            score += 5

        # Too far from MA20
        if abs(row["DISTANCE_MA20"]) > 25:
            score -= 10

        # =================================
        # FINAL SCORE LIMIT
        # =================================

        if score > 100:
            score = 100

        if score < 0:
            score = 0

        return int(score)

    except Exception as e:

        print(f"❌ Scoring Error: {e}")

        return 0
