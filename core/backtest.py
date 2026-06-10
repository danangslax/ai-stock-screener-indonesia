import pandas as pd

from backtesting import (
    Backtest,
    Strategy
)

from core.data_loader import (
    load_stock_data
)

from core.indicators import (
    add_indicators
)

# ======================================
# SWING STRATEGY
# ======================================

class SwingStrategy(Strategy):

    # ======================================
    # INIT
    # ======================================

    def init(self):

        pass

    # ======================================
    # NEXT BAR
    # ======================================

    def next(self):

        price = self.data.Close[-1]

        ma5 = self.data.MA5[-1]

        ma20 = self.data.MA20[-1]

        rsi = self.data.RSI[-1]

        volume = self.data.Volume[-1]

        vol_ma20 = self.data.VOL_MA20[-1]

        adx = self.data.ADX[-1]

        # ======================================
        # BUY CONDITION
        # ======================================

        bullish_trend = (

            price > ma5

            and

            price > ma20

            and

            ma5 > ma20
        )

        bullish_momentum = (

            50 <= rsi <= 75
        )

        bullish_volume = (

            volume > (
                1.5 * vol_ma20
            )
        )

        strong_trend = (

            adx > 20
        )

        if (

            bullish_trend

            and

            bullish_momentum

            and

            bullish_volume

            and

            strong_trend
        ):

            if not self.position:

                self.buy()

        # ======================================
        # SELL CONDITION
        # ======================================

        if self.position:

            # ======================================
            # STOP LOSS
            # ======================================

            if (

                price

                <

                (
                    self.position
                    .entry_price
                    * 0.95
                )
            ):

                self.position.close()

            # ======================================
            # TAKE PROFIT
            # ======================================

            elif (

                price

                >

                (
                    self.position
                    .entry_price
                    * 1.10
                )
            ):

                self.position.close()

# ======================================
# RUN BACKTEST
# ======================================

def run_backtest(

    symbol,

    period="1y",

    interval="1d",

    cash=100_000_000
):

    try:

        # ======================================
        # LOAD DATA
        # ======================================

        df = load_stock_data(

            symbol,

            period=period,

            interval=interval
        )

        # ======================================
        # VALIDATION
        # ======================================

        if df.empty:

            print(
                f"Empty data: {symbol}"
            )

            return None

        if len(df) < 60:

            print(
                f"Insufficient data: {symbol}"
            )

            return None

        # ======================================
        # ADD INDICATORS
        # ======================================

        df = add_indicators(df)

        # ======================================
        # CLEAN DATA
        # ======================================

        df = df.dropna()

        if df.empty:

            print(
                f"Indicator data empty: "
                f"{symbol}"
            )

            return None

        # ======================================
        # BACKTEST ENGINE
        # ======================================

        bt = Backtest(

            df,

            SwingStrategy,

            cash=cash,

            commission=0.0015,

            exclusive_orders=True
        )

        # ======================================
        # RUN BACKTEST
        # ======================================

        stats = bt.run()

        return stats

    except Exception as e:

        print(

            f"BACKTEST ERROR "
            f"{symbol}: {e}"
        )

        return None