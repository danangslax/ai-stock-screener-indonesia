import yfinance as yf
import pandas as pd

# ======================================
# MORNING CONFIRMATION
# ======================================

def morning_confirmation(symbol):

    try:

        # ======================================
        # DOWNLOAD INTRADAY DATA
        # ======================================

        df = yf.download(
            symbol,
            period="2d",
            interval="15m",
            auto_adjust=True,
            progress=False
        )

        # ======================================
        # FIX MULTI INDEX
        # ======================================

        if isinstance(df.columns, pd.MultiIndex):

            df.columns = (
                df.columns.get_level_values(0)
            )

        if df.empty:

            return "NO DATA"

        # ======================================
        # VALIDATION
        # ======================================

        if len(df) < 10:

            return "NO DATA"

        # ======================================
        # LATEST DATA
        # ======================================

        latest = df.iloc[-1]

        current_price = latest["Close"]

        current_volume = latest["Volume"]

        open_price = latest["Open"]

        high_price = latest["High"]

        low_price = latest["Low"]

        # ======================================
        # YESTERDAY CLOSE
        # ======================================

        daily = yf.download(
            symbol,
            period="5d",
            interval="1d",
            auto_adjust=True,
            progress=False
        )

        if isinstance(daily.columns, pd.MultiIndex):

            daily.columns = (
                daily.columns.get_level_values(0)
            )

        yesterday_close = (
            daily.iloc[-2]["Close"]
        )

        # ======================================
        # GAP %
        # ======================================

        gap_percent = (
            (open_price - yesterday_close)
            / yesterday_close
        ) * 100

        # ======================================
        # CANDLE ANALYSIS
        # ======================================

        candle_body = (
            current_price - open_price
        )

        candle_range = (
            high_price - low_price
        )

        upper_wick = (
            high_price -
            max(current_price, open_price)
        )

        # ======================================
        # BUY CONDITIONS
        # ======================================

        if (
            current_price > yesterday_close
            and candle_body > 0
            and gap_percent < 8
            and upper_wick < (
                candle_range * 0.4
            )
        ):

            return "BUY"

        # ======================================
        # AVOID CONDITIONS
        # ======================================

        if (
            gap_percent > 10
            or candle_body < 0
        ):

            return "AVOID"

        # ======================================
        # DEFAULT
        # ======================================

        return "WATCH"

    except Exception as e:

        print(
            f"CONFIRMATION ERROR {symbol}: {e}"
        )

        return "ERROR"