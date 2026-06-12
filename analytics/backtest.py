import pandas as pd

from backtesting import (
    Backtest,
    Strategy,
)

from storage.data_loader import load_stock_data

from ai.ai_parameters import load_parameters

from infrastructure.logger import logger

# ======================================
# SWING STRATEGY
# ======================================


class SwingStrategy(Strategy):

    # ======================================
    # DEFAULT PARAMETERS
    # ======================================

    min_rsi = 50

    min_adx = 20

    stop_loss_pct = 0.05

    take_profit_pct = 0.10

    volume_multiplier = 1.5

    # ======================================
    # INIT
    # ======================================

    def init(self):

        pass

    # ======================================
    # NEXT
    # ======================================

    def next(self):

        try:

            price = self.data.Close[-1]

            ma5 = self.data.MA5[-1]

            ma20 = self.data.MA20[-1]

            ema20 = self.data.EMA20[-1]

            ema50 = self.data.EMA50[-1]

            rsi = self.data.RSI[-1]

            adx = self.data.ADX[-1]

            volume = self.data.Volume[-1]

            vol_ma20 = self.data.VOL_MA20[-1]

            # ======================================
            # BUY CONDITIONS
            # ======================================

            bullish_structure = price > ma5 and price > ma20 and ema20 > ema50

            momentum = rsi >= self.min_rsi and adx >= self.min_adx

            volume_confirmation = volume > (self.volume_multiplier * vol_ma20)

            # ======================================
            # ENTRY
            # ======================================

            if bullish_structure and momentum and volume_confirmation:

                if not self.position:

                    self.buy()

            # ======================================
            # EXIT MANAGEMENT
            # ======================================

            if self.position:

                stop_price = self.position.entry_price * (1 - self.stop_loss_pct)

                take_profit_price = self.position.entry_price * (
                    1 + self.take_profit_pct
                )

                # STOP LOSS
                if price <= stop_price:

                    self.position.close()

                # TAKE PROFIT
                elif price >= take_profit_price:

                    self.position.close()

        except Exception as e:

            logger.error(f"Strategy error: {e}")


# ======================================
# RUN BACKTEST
# ======================================


def run_backtest(
    symbol,
    period="1y",
    initial_cash=100_000_000,
    commission=0.0015,
):

    try:

        logger.info(f"Running backtest " f"{symbol}")

        # ======================================
        # LOAD PARAMETERS
        # ======================================

        parameters = load_parameters()

        # ======================================
        # LOAD DATA
        # ======================================

        df = load_stock_data(
            symbol,
            period=period,
            interval="1d",
            cache_only=True,
        )

        # ======================================
        # VALIDATION
        # ======================================

        if df.empty:

            logger.warning(f"Empty data " f"{symbol}")

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
            "EMA20",
            "EMA50",
            "RSI",
            "ADX",
            "VOL_MA20",
        ]

        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:

            logger.warning(f"Missing columns " f"{symbol}: " f"{missing_columns}")

            return None

        # ======================================
        # CLEAN DATA
        # ======================================

        df = df.copy()

        df = df.dropna()

        df = df.sort_index()

        # ======================================
        # VALIDATION
        # ======================================

        if len(df) < 100:

            logger.warning(f"Not enough data " f"{symbol}")

            return None

        # ======================================
        # APPLY AI PARAMETERS
        # ======================================

        SwingStrategy.min_rsi = parameters.get("min_rsi", 50)

        SwingStrategy.min_adx = parameters.get("min_adx", 20)

        SwingStrategy.stop_loss_pct = 0.05

        SwingStrategy.take_profit_pct = 0.10

        # ======================================
        # BACKTEST ENGINE
        # ======================================

        bt = Backtest(
            df,
            SwingStrategy,
            cash=initial_cash,
            commission=commission,
            exclusive_orders=True,
        )

        # ======================================
        # RUN
        # ======================================

        stats = bt.run()

        # ======================================
        # CLEAN RESULT
        # ======================================

        result = {
            "symbol": symbol,
            "return_pct": round(stats["Return [%]"], 2),
            "buy_hold_return": round(stats["Buy & Hold Return [%]"], 2),
            "max_drawdown": round(stats["Max. Drawdown [%]"], 2),
            "winrate": round(stats["Win Rate [%]"], 2),
            "profit_factor": round(stats["Profit Factor"], 2),
            "sharpe_ratio": round(stats["Sharpe Ratio"], 2),
            "total_trades": int(stats["# Trades"]),
            "expectancy": round(stats["Expectancy [%]"], 2),
        }

        # ======================================
        # SURVIVABILITY
        # ======================================

        survivability = "WEAK"

        if (
            result["winrate"] >= 55
            and result["profit_factor"] >= 1.5
            and abs(result["max_drawdown"]) <= 15
        ):

            survivability = "ROBUST"

        elif result["winrate"] >= 45 and result["profit_factor"] >= 1:

            survivability = "STABLE"

        result["survivability"] = survivability

        # ======================================
        # AI SCORE
        # ======================================

        ai_score = round(
            (result["winrate"] * 0.35)
            + (result["profit_factor"] * 20)
            + (max(0, 20 - abs(result["max_drawdown"])) * 1.5),
            2,
        )

        ai_score = min(ai_score, 100)

        result["ai_score"] = ai_score

        logger.info(f"Backtest completed " f"{symbol}")

        return result

    except Exception as e:

        logger.error(f"BACKTEST ERROR " f"{symbol}: {e}")

        return None
