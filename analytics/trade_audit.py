from storage.data_loader import load_stock_data

from infrastructure.notifier import send_telegram_message

from infrastructure.logger import logger

from trading.trade_manager import manage_open_trades

from trading.paper_trading import load_open_trades

# ======================================
# TRADE AUDIT ENGINE
# ======================================


def run_trade_audit(market_regime="UNKNOWN"):

    try:

        # ======================================
        # LOAD OPEN TRADES
        # ======================================

        trades = load_open_trades()

        if not trades:

            logger.warning("No open trades")

            return {
                "total": 0,
                "closed": 0,
                "active": 0,
            }

        logger.info(f"Auditing " f"{len(trades)} trades")

        # ======================================
        # MARKET PRICES
        # ======================================

        market_prices = {}

        # ======================================
        # LOAD MARKET DATA
        # ======================================

        for trade in trades:

            try:

                symbol = trade["symbol"]

                df = load_stock_data(symbol, period="5d", interval="1d")

                if df.empty:

                    logger.warning(f"No data: " f"{symbol}")

                    continue

                latest = df.iloc[-1]

                market_prices[symbol] = float(latest["Close"])

            except Exception as e:

                logger.error(f"Market data error | " f"{trade.get('symbol')} | " f"{e}")

        # ======================================
        # MANAGE TRADES
        # ======================================

        actions = manage_open_trades(market_prices, market_regime)

        # ======================================
        # SEND ALERTS
        # ======================================

        for action in actions:

            try:

                symbol = action["symbol"]

                action_type = action["action"]

                price = action["price"]

                pnl = action["pnl_percent"]

                emoji = "⚠️"

                if action_type == "TAKE PROFIT":

                    emoji = "🚀"

                elif action_type == "STOP LOSS":

                    emoji = "❌"

                elif action_type == "PANIC EXIT":

                    emoji = "🔥"

                message = f"""
{emoji} <b>TRADE AUDIT ALERT</b>

📈 Symbol:
{symbol}

🎯 Action:
{action_type}

💰 Exit Price:
{price:.2f}

📊 PnL:
{pnl:.2f}%

🌍 Market Regime:
{market_regime}

🤖 Trade managed automatically
"""

                send_telegram_message(message)

            except Exception as notify_error:

                logger.error(f"Notification error: " f"{notify_error}")

        # ======================================
        # SUMMARY
        # ======================================

        summary = {
            "total": len(trades),
            "closed": len(actions),
            "active": (len(trades) - len(actions)),
        }

        logger.info(f"Trade audit complete | " f"Closed={summary['closed']}")

        return summary

    except Exception as e:

        logger.error(f"Audit Engine Error: " f"{e}")

        return {
            "total": 0,
            "closed": 0,
            "active": 0,
        }
