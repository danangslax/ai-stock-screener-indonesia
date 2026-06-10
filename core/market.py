from core.data_loader import (
    load_stock_data
)

from core.indicators import (
    add_indicators
)

# ======================================
# MARKET STATUS ENGINE
# ======================================

def get_market_status():

    try:

        # ======================================
        # LOAD IHSG DATA
        # ======================================

        ihsg = load_stock_data(
            "^JKSE",
            period="6mo"
        )

        # ======================================
        # VALIDATION
        # ======================================

        if ihsg.empty:

            return {
                "status": "UNKNOWN",
                "change": 0,
                "rsi": 0
            }

        # ======================================
        # ADD INDICATORS
        # ======================================

        ihsg = add_indicators(ihsg)

        if ihsg.empty or len(ihsg) < 2:

            return {
                "status": "UNKNOWN",
                "change": 0,
                "rsi": 0
            }

        # ======================================
        # LATEST DATA
        # ======================================

        latest = ihsg.iloc[-1]

        previous = ihsg.iloc[-2]

        close_price = latest["Close"]

        daily_change = (
            (
                close_price
                - previous["Close"]
            )
            / previous["Close"]
        ) * 100

        rsi = latest["RSI"]

        ema20 = latest["EMA20"]

        ema50 = latest["EMA50"]

        adx = latest["ADX"]

        # ======================================
        # MARKET REGIME
        # ======================================

        # STRONG BULLISH
        if (
            close_price > ema20
            and ema20 > ema50
            and rsi >= 60
            and adx >= 25
        ):

            status = "STRONG BULLISH"

        # BULLISH
        elif (
            close_price > ema20
            and rsi >= 50
        ):

            status = "BULLISH"

        # STRONG BEARISH
        elif (
            close_price < ema20
            and ema20 < ema50
            and rsi < 40
        ):

            status = "STRONG BEARISH"

        # BEARISH
        elif (
            close_price < ema20
            and rsi < 50
        ):

            status = "BEARISH"

        # SIDEWAYS
        else:

            status = "SIDEWAYS"

        # ======================================
        # RETURN DATA
        # ======================================

        return {

            "status": status,

            "change": round(
                daily_change,
                2
            ),

            "rsi": round(
                rsi,
                2
            ),

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

            "adx": round(
                adx,
                2
            )
        }

    except Exception as e:

        print(
            f"❌ Market Status Error: {e}"
        )

        return {

            "status": "ERROR",

            "change": 0,

            "rsi": 0,

            "close": 0,

            "ema20": 0,

            "ema50": 0,

            "adx": 0
        }