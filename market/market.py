import pandas as pd

from infrastructure.logger import logger

from storage.data_loader import load_stock_data

from storage.indicators import add_indicators

# ======================================
# MARKET SYMBOL
# ======================================

MARKET_SYMBOL = "^JKSE"

# ======================================
# GET MARKET STATUS
# ======================================


def get_market_status():

    try:

        logger.info("Analyzing IHSG")

        # ======================================
        # LOAD MARKET DATA
        # ======================================

        df = load_stock_data(MARKET_SYMBOL, period="1y", interval="1d", use_cache=True)

        # ======================================
        # VALIDATION
        # ======================================

        if df.empty:

            logger.warning("IHSG data empty")

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

            logger.warning("IHSG indicator failed")

            return {"status": "UNKNOWN"}

        # ======================================
        # LATEST DATA
        # ======================================

        latest = df.iloc[-1]

        previous = df.iloc[-2]

        # ======================================
        # BASIC DATA
        # ======================================

        close = float(latest["Close"])

        previous_close = float(previous["Close"])

        ma20 = float(latest["MA20"])

        ma50 = float(latest["MA50"])

        ema20 = float(latest["EMA20"])

        ema50 = float(latest["EMA50"])

        rsi = float(latest["RSI"])

        adx = float(latest["ADX"])

        volatility = float(latest["VOLATILITY"])

        monthly_return = float(latest["MONTHLY_RETURN"])

        # ======================================
        # NAN VALIDATION
        # ======================================

        metrics = [
            close,
            ma20,
            ma50,
            ema20,
            ema50,
            rsi,
            adx,
            volatility,
            monthly_return,
        ]

        if any(pd.isna(v) for v in metrics):

            logger.warning("Invalid IHSG metrics")

            return {"status": "UNKNOWN"}

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
        # DISTRIBUTION
        # ======================================

        elif close < ma20 and rsi < 50 and volatility > 0.02:

            status = "DISTRIBUTION"

        # ======================================
        # RECOVERY
        # ======================================

        elif close > ma20 and rsi > 45 and monthly_return > 0:

            status = "RECOVERY"

        # ======================================
        # DAILY CHANGE
        # ======================================

        change = round(((close - previous_close) / previous_close) * 100, 2)

        logger.info(f"Market Regime: {status}")

        return {
            "symbol": MARKET_SYMBOL,
            "status": status,
            "change": change,
            "close": close,
            "rsi": round(rsi, 2),
            "adx": round(adx, 2),
            "volatility": round(volatility, 4),
            "monthly_return": round(monthly_return, 4),
            "data_points": len(df),
        }

    except Exception as e:

        logger.error(f"Market Error: {e}")

        return {"status": "UNKNOWN"}
