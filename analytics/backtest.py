import pandas as pd

from backtesting import Backtest, Strategy

from storage.data_loader import load_stock_data

# ======================================
# SWING STRATEGY
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

            # STOP LOSS
            if price < (self.position.entry_price * 0.95):

                self.position.close()

            # TAKE PROFIT
            elif price > (self.position.entry_price * 1.10):

                self.position.close()


# ======================================
# RUN BACKTEST
# ======================================


def run_backtest(symbol, period="1y"):

    try:

        print(f"🧪 Running backtest " f"{symbol}")

        # ======================================
        # LOAD ENRICHED CACHE
        # ======================================

        df = load_stock_data(symbol, period=period, interval="1d", cache_only=True)

        # ======================================
        # VALIDATION
        # ======================================

        if df.empty:

            print(f"⚠️ Empty data " f"{symbol}")

            return None

        # ======================================
        # REQUIRED COLUMNS
        # ======================================

        required_columns = [
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "MA5",
            "MA20",
            "RSI",
            "VOL_MA20",
        ]

        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:

            print(f"⚠️ Missing columns " f"{symbol}: " f"{missing_columns}")

            return None

        # ======================================
        # REMOVE NAN
        # ======================================

        df = df.dropna()

        # ======================================
        # VALIDATION
        # ======================================

        if len(df) < 50:

            print(f"⚠️ Not enough data " f"{symbol}")

            return None

        # ======================================
        # BACKTEST ENGINE
        # ======================================

        bt = Backtest(
            df,
            SwingStrategy,
            cash=100_000_000,
            commission=0.0015,
            exclusive_orders=True,
        )

        # ======================================
        # RUN BACKTEST
        # ======================================

        stats = bt.run()

        print(f"✅ Backtest completed " f"{symbol}")

        return stats

    except Exception as e:

        print(f"❌ BACKTEST ERROR " f"{symbol}: {e}")

        return None
