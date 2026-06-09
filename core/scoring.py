# ======================================
# AI SCORING SYSTEM
# ======================================

def calculate_score(row, df):

    score = 0

    # =================================
    # TREND STRUCTURE
    # =================================

    # Price above MA5
    if row["Close"] > row["MA5"]:
        score += 20

    # Price above MA20
    if row["Close"] > row["MA20"]:
        score += 20

    # MA5 above MA20
    if row["MA5"] > row["MA20"]:
        score += 10

    # =================================
    # RSI MOMENTUM
    # =================================

    # Bullish momentum
    if row["RSI"] >= 50:
        score += 15

    # Strong momentum
    if row["RSI"] >= 60:
        score += 10

    # Overheat penalty
    if row["RSI"] >= 75:
        score -= 10

    # =================================
    # VOLUME ANALYSIS
    # =================================

    # Volume above average
    if row["Volume"] > row["VOL_MA20"]:
        score += 15

    # Strong volume breakout
    if row["Volume"] > (1.5 * row["VOL_MA20"]):
        score += 15

    # =================================
    # BOLLINGER POSITION
    # =================================

    # Above BB middle
    if row["Close"] > row["BB_MIDDLE"]:
        score += 10

    # Above BB upper = momentum expansion
    if row["Close"] > row["BB_UPPER"]:
        score += 10

    # =================================
    # BREAKOUT DETECTION
    # =================================

    highest_20 = df["High"].rolling(20).max()

    # Breakout 20-day high
    if row["Close"] >= highest_20.iloc[-2]:
        score += 20

    # =================================
    # MOMENTUM NOT TOO LATE
    # =================================

    weekly_return = (
        row["Close"] /
        df["Close"].iloc[-6]
    ) - 1

    # Sweet spot momentum
    if 0.05 <= weekly_return <= 0.30:
        score += 10

    # Too extended
    if weekly_return > 0.30:
        score -= 10

    # =================================
    # FINAL SCORE LIMIT
    # =================================

    if score > 100:
        score = 100

    if score < 0:
        score = 0

    return score