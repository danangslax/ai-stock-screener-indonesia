import pandas as pd
import yfinance as yf

from storage.indicators import add_indicators

# ======================================
# GET MARKET STATUS
# ======================================


def get_market_status():

    try:

        print("📈 Analyzing IHSG")

        # ======================================
        # DOWNLOAD IHSG
        # ======================================

        df = yf.download(
            "^JKSE", period="1y", interval="1d", auto_adjust=True, progress=False
        )

        # ======================================
        # VALIDATION
        # ======================================

        if df.empty:

            return {"status": "UNKNOWN"}

        # ======================================
        # FIX MULTI INDEX
        # ======================================

        if isinstance(df.columns, pd.MultiIndex):

            df.columns = df.columns.get_level_values(0)

        # ======================================
        # ADD INDICATORS
        # ======================================

        df = add_indicators(df)

        if df.empty:

            return {"status": "UNKNOWN"}

        latest = df.iloc[-1]

        # ======================================
        # BASIC DATA
        # ======================================

        close = float(latest["Close"])

        ma20 = float(latest["MA20"])

        ma50 = float(latest["MA50"])

        ema20 = float(latest["EMA20"])

        ema50 = float(latest["EMA50"])

        rsi = float(latest["RSI"])

        adx = float(latest["ADX"])

        volatility = float(latest["VOLATILITY"])

        monthly_return = float(latest["MONTHLY_RETURN"])

        # ======================================
        # DEFAULT STATUS
        # ======================================

        status = "SIDEWAYS"

        # ======================================
        # STRONG BULL
        # ======================================

        if (
            close > ma20 > ma50
            and ema20 > ema50
            and rsi >= 65
            and adx >= 25
            and monthly_return > 0.08
        ):

            status = "STRONG_BULL"

        # ======================================
        # BULL
        # ======================================

        elif close > ma20 and ma20 > ma50 and rsi >= 55:

            status = "BULL"

        # ======================================
        # ACCUMULATION
        # ======================================

        elif close > ma50 and 45 <= rsi <= 60 and adx < 20:

            status = "ACCUMULATION"

        # ======================================
        # DISTRIBUTION
        # ======================================

        elif close < ma20 and rsi < 50 and volatility > 0.02:

            status = "DISTRIBUTION"

        # ======================================
        # PANIC
        # ======================================

        elif close < ma20 and close < ma50 and rsi < 35 and volatility > 0.04:

            status = "PANIC"

        # ======================================
        # BEARISH
        # ======================================

        elif close < ma20 and close < ma50:

            status = "BEARISH"

        # ======================================
        # RECOVERY
        # ======================================

        elif close > ma20 and rsi > 45 and monthly_return > 0:

            status = "RECOVERY"

        # ======================================
        # DAILY CHANGE
        # ======================================

        previous_close = float(df.iloc[-2]["Close"])

        change = round(((close - previous_close) / previous_close) * 100, 2)

        print(f"🌍 Market Regime: " f"{status}")

        return {
            "status": status,
            "change": change,
            "close": close,
            "rsi": round(rsi, 2),
            "adx": round(adx, 2),
            "volatility": round(volatility, 4),
            "monthly_return": round(monthly_return, 4),
        }

    except Exception as e:

        print(f"❌ Market Error: {e}")

        return {"status": "UNKNOWN"}
