from core.data_loader import (
    load_stock_data
)

from core.indicators import (
    add_indicators
)

# ======================================
# MORNING CONFIRMATION ENGINE
# ======================================

def morning_confirmation(symbol):

    try:

        # ======================================
        # LOAD INTRADAY DATA
        # ======================================

        intraday = load_stock_data(

            symbol,

            period="5d",

            interval="15m"
        )

        # ======================================
        # VALIDATION
        # ======================================

        if intraday.empty:

            return "NO DATA"

        if len(intraday) < 30:

            return "NO DATA"

        # ======================================
        # ADD INDICATORS
        # ======================================

        intraday = add_indicators(
            intraday
        )

        if intraday.empty:

            return "NO DATA"

        # ======================================
        # LOAD DAILY DATA
        # ======================================

        daily = load_stock_data(
            symbol,
            period="3mo",
            interval="1d"
        )

        daily = add_indicators(daily)

        if daily.empty:

            return "NO DATA"

        # ======================================
        # LATEST DATA
        # ======================================

        latest = intraday.iloc[-1]

        previous = intraday.iloc[-2]

        daily_latest = daily.iloc[-1]

        # ======================================
        # PRICE DATA
        # ======================================

        current_price = float(
            latest["Close"]
        )

        open_price = float(
            latest["Open"]
        )

        high_price = float(
            latest["High"]
        )

        low_price = float(
            latest["Low"]
        )

        previous_close = float(
            daily.iloc[-2]["Close"]
        )

        # ======================================
        # VOLUME DATA
        # ======================================

        current_volume = float(
            latest["Volume"]
        )

        average_volume = float(
            latest["VOL_MA20"]
        )

        # ======================================
        # MOMENTUM DATA
        # ======================================

        rsi = float(
            latest["RSI"]
        )

        macd = float(
            latest["MACD"]
        )

        macd_signal = float(
            latest["MACD_SIGNAL"]
        )

        adx = float(
            latest["ADX"]
        )

        # ======================================
        # GAP ANALYSIS
        # ======================================

        gap_percent = (
            (
                open_price
                - previous_close
            )
            / previous_close
        ) * 100

        # ======================================
        # CANDLE ANALYSIS
        # ======================================

        candle_body = (
            current_price
            - open_price
        )

        candle_range = (
            high_price
            - low_price
        )

        upper_wick = (
            high_price
            - max(
                current_price,
                open_price
            )
        )

        lower_wick = (
            min(
                current_price,
                open_price
            )
            - low_price
        )

        # ======================================
        # VOLUME CONFIRMATION
        # ======================================

        volume_ratio = (
            current_volume
            / average_volume
        )

        # ======================================
        # TREND CONFIRMATION
        # ======================================

        bullish_trend = (

            current_price
            > daily_latest["EMA20"]

            and

            daily_latest["EMA20"]
            > daily_latest["EMA50"]
        )

        # ======================================
        # STRONG BUY
        # ======================================

        if (

            bullish_trend

            and

            current_price
            > previous_close

            and

            candle_body > 0

            and

            volume_ratio >= 1.5

            and

            rsi >= 60

            and

            macd > macd_signal

            and

            adx >= 20

            and

            gap_percent < 8

            and

            upper_wick < (
                candle_range * 0.35
            )
        ):

            return "STRONG BUY"

        # ======================================
        # BUY
        # ======================================

        if (

            bullish_trend

            and

            current_price
            > previous_close

            and

            candle_body > 0

            and

            rsi >= 50

            and

            gap_percent < 10
        ):

            return "BUY"

        # ======================================
        # AVOID CONDITIONS
        # ======================================

        if (

            gap_percent > 12

            or

            candle_body < 0

            or

            rsi < 45

            or

            current_price
            < daily_latest["EMA20"]
        ):

            return "AVOID"

        # ======================================
        # WEAK MOMENTUM
        # ======================================

        if (

            volume_ratio < 0.8

            or

            adx < 15
        ):

            return "WEAK"

        # ======================================
        # DEFAULT
        # ======================================

        return "WATCH"

    except Exception as e:

        print(
            f"❌ Confirmation Error "
            f"{symbol}: {e}"
        )

        return "ERROR"