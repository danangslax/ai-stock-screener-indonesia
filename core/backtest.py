import pandas as pd
import yfinance as yf

from backtesting import Backtest
from backtesting import Strategy

from core.indicators import add_indicators

# ======================================
# STRATEGY
# ======================================

class SwingStrategy(Strategy):

    def init(self):
        pass

    def next(self):

        price = self.data.Close[-1]

        ma5 = self.data.MA5[-1]

        ma20 = self.data.MA20[-1]

        rsi = self.data.RSI[-1]

        volume = self.data.Volume[-1]

        vol_ma20 = self.data.VOL_MA20[-1]

        # ======================================
        # BUY CONDITION
        # ======================================

        if (
            price > ma5
            and price > ma20
            and ma5 > ma20
            and 50 <= rsi <= 75
            and volume > (1.5 * vol_ma20)
        ):

            if not self.position:

                self.buy()

        # ======================================
        # SELL CONDITION
        # ======================================

        if self.position:

            # stop loss
            if price < (self.position.entry_price * 0.95):

                self.position.close()

            # take profit
            elif price > (
                self.position.entry_price * 1.10
            ):

                self.position.close()

# ======================================
# RUN BACKTEST
# ======================================

def run_backtest(symbol):

    try:

        # ======================================
        # DOWNLOAD DATA
        # ======================================

        df = yf.download(
            symbol,
            period="1y",
            interval="1d",
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

            return None

        # ======================================
        # ADD INDICATORS
        # ======================================

        df = add_indicators(df)

        # ======================================
        # BACKTEST
        # ======================================

        bt = Backtest(
            df,
            SwingStrategy,
            cash=100_000_000,
            commission=0.0015
        )

        stats = bt.run()

        return stats

    except Exception as e:

        print(
            f"BACKTEST ERROR {symbol}: {e}"
        )

        return None