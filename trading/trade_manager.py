from core.paper_trading import load_trades, save_trades

# ======================================
# CLOSE TRADE
# ======================================


def close_trade(symbol, exit_price):

    try:

        trades = load_trades()

        for trade in trades:

            if trade["symbol"] == symbol and trade["status"] == "OPEN":

                entry_price = trade["buy_price"]

                quantity = trade["quantity"]

                pnl = (exit_price - entry_price) * quantity

                trade["exit_price"] = exit_price

                trade["profit_loss"] = round(pnl, 2)

                trade["status"] = "CLOSED"

        save_trades(trades)

        return True

    except Exception as e:

        print(f"❌ Close trade error: " f"{e}")

        return False
