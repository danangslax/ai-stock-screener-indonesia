import pandas as pd

# ======================================
# DAILY TIMEFRAME ANALYSIS
# ======================================

def analyze_daily_timeframe(df):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if df.empty:

            return None

        if len(df) < 200:

            return None

        latest = df.iloc[-1]

        previous = df.iloc[-2]

        # ======================================
        # REQUIRED COLUMNS
        # ======================================

        required_columns = [

            "EMA20",

            "EMA50",

            "EMA200",

            "RSI",

            "ADX",

            "MACD",

            "MACD_SIGNAL"
        ]

        for col in required_columns:

            if col not in df.columns:

                return None

        # ======================================
        # BASIC DATA
        # ======================================

        close_price = float(
            latest["Close"]
        )

        ema20 = float(
            latest["EMA20"]
        )

        ema50 = float(
            latest["EMA50"]
        )

        ema200 = float(
            latest["EMA200"]
        )

        rsi = float(
            latest["RSI"]
        )

        adx = float(
            latest["ADX"]
        )

        macd = float(
            latest["MACD"]
        )

        macd_signal = float(
            latest["MACD_SIGNAL"]
        )

        # ======================================
        # SCORE
        # ======================================

        score = 0

        # ======================================
        # TREND STRUCTURE
        # ======================================

        # Price above EMA20
        if close_price > ema20:

            score += 15

        # EMA20 above EMA50
        if ema20 > ema50:

            score += 20

        # EMA50 above EMA200
        if ema50 > ema200:

            score += 25

        # Perfect bullish structure
        if (

            close_price > ema20

            and

            ema20 > ema50

            and

            ema50 > ema200
        ):

            score += 20

        # ======================================
        # MOMENTUM
        # ======================================

        # RSI bullish
        if rsi >= 50:

            score += 10

        # RSI strong
        if rsi >= 65:

            score += 5

        # ======================================
        # TREND STRENGTH
        # ======================================

        if adx >= 18:

            score += 10

        if adx >= 35:

            score += 5

        # ======================================
        # MACD CONFIRMATION
        # ======================================

        if macd > macd_signal:

            score += 10

        # MACD crossover
        if (

            previous["MACD"]

            <

            previous["MACD_SIGNAL"]

            and

            macd > macd_signal
        ):

            score += 10

        # ======================================
        # SCORE LIMIT
        # ======================================

        if score > 100:

            score = 100

        # ======================================
        # TREND STATUS
        # ======================================

        if score >= 75:

            trend_status = (
                "STRONG BULLISH"
            )

        elif score >= 60:

            trend_status = (
                "BULLISH"
            )

        elif score >= 50:

            trend_status = (
                "NEUTRAL"
            )

        else:

            trend_status = (
                "WEAK"
            )

        # ======================================
        # RETURN RESULT
        # ======================================

        return {

            "score": score,

            "status": trend_status,

            "close": round(
                close_price,
                2
            ),

            "ema20": round(
                ema20,
                2
            ),

            "ema50": round(
                ema50,
                2
            ),

            "ema200": round(
                ema200,
                2
            ),

            "rsi": round(
                rsi,
                2
            ),

            "adx": round(
                adx,
                2
            ),

            "macd": round(
                macd,
                2
            )
        }

    except Exception as e:

        print(
            f"DAILY TIMEFRAME ERROR: "
            f"{e}"
        )

        return None