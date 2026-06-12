from trading.paper_trading import (
    close_trade,
    load_open_trades,
)

from infrastructure.logger import logger

# ======================================
# MANAGE OPEN TRADES
# ======================================


def manage_open_trades(market_prices, market_regime="UNKNOWN"):

    try:

        # ======================================
        # LOAD OPEN TRADES
        # ======================================

        open_trades = load_open_trades()

        if not open_trades:

            logger.info("No open trades found")

            return []

        # ======================================
        # RESULT
        # ======================================

        actions = []

        # ======================================
        # LOOP TRADES
        # ======================================

        for trade in open_trades:

            try:

                symbol = trade["symbol"]

                trade_id = trade["id"]

                stop_loss = float(trade["stop_loss"])

                take_profit = float(trade["take_profit"])

                buy_price = float(trade["buy_price"])

                # ======================================
                # MARKET PRICE
                # ======================================

                current_price = market_prices.get(symbol)

                if current_price is None:

                    logger.warning(f"Missing market " f"price: {symbol}")

                    continue

                # ======================================
                # PNL %
                # ======================================

                pnl_percent = round(((current_price - buy_price) / buy_price) * 100, 2)

                # ======================================
                # STOP LOSS
                # ======================================

                if current_price <= stop_loss:

                    close_trade(trade_id, current_price, close_reason="STOP_LOSS")

                    actions.append(
                        {
                            "symbol": symbol,
                            "action": ("STOP LOSS"),
                            "price": (current_price),
                            "pnl_percent": (pnl_percent),
                        }
                    )

                    logger.info(f"STOP LOSS | " f"{symbol}")

                    continue

                # ======================================
                # TAKE PROFIT
                # ======================================

                if current_price >= take_profit:

                    close_trade(trade_id, current_price, close_reason="TAKE_PROFIT")

                    actions.append(
                        {
                            "symbol": symbol,
                            "action": ("TAKE PROFIT"),
                            "price": (current_price),
                            "pnl_percent": (pnl_percent),
                        }
                    )

                    logger.info(f"TAKE PROFIT | " f"{symbol}")

                    continue

                # ======================================
                # PANIC MARKET
                # ======================================

                if market_regime == "PANIC":

                    if pnl_percent < -3:

                        close_trade(
                            trade_id, current_price, close_reason=("PANIC_EXIT")
                        )

                        actions.append(
                            {
                                "symbol": (symbol),
                                "action": ("PANIC EXIT"),
                                "price": (current_price),
                                "pnl_percent": (pnl_percent),
                            }
                        )

                        logger.warning(f"PANIC EXIT | " f"{symbol}")

            except Exception as trade_error:

                logger.error(f"Trade manager " f"symbol error: " f"{trade_error}")

        logger.info(f"Trade manager complete | " f"Actions={len(actions)}")

        return actions

    except Exception as e:

        logger.error(f"Trade manager error: " f"{e}")

        return []
