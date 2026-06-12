from storage.data_loader import load_stock_data

from core.notifier import send_telegram_message

from core.paper_trading import load_open_trades, close_trade

# ======================================
# TRADE AUDIT ENGINE
# ======================================


def run_trade_audit():

    try:

        # ======================================
        # LOAD OPEN TRADES
        # ======================================

        trades = load_open_trades()

        if not trades:

            print("⚠️ No open trades")

            return

        print(f"📊 Auditing " f"{len(trades)} trades")

        # ======================================
        # LOOP TRADES
        # ======================================

        for trade in trades:

            try:

                symbol = trade["symbol"]

                trade_id = trade["id"]

                buy_price = float(trade["buy_price"])

                stop_loss = float(trade["stop_loss"])

                take_profit = float(trade["take_profit"])

                quantity = int(trade["quantity"])

                # ======================================
                # LOAD LATEST PRICE
                # ======================================

                df = load_stock_data(symbol, period="5d", interval="1d")

                if df.empty:

                    print(f"⚠️ No data: {symbol}")

                    continue

                latest = df.iloc[-1]

                current_price = float(latest["Close"])

                # ======================================
                # CALCULATE PNL
                # ======================================

                pnl = (current_price - buy_price) * quantity

                pnl_percent = ((current_price - buy_price) / buy_price) * 100

                print(
                    f"📈 {symbol} | "
                    f"Price: {current_price:.2f} | "
                    f"PnL: {pnl_percent:.2f}%"
                )

                # ======================================
                # STOP LOSS HIT
                # ======================================

                if current_price <= stop_loss:

                    close_trade(trade_id, current_price, close_reason="STOP LOSS")

                    message = f"""
❌ <b>STOP LOSS HIT</b>

📉 {symbol}

💰 Buy: {buy_price:.2f}
💸 Sell: {current_price:.2f}

📊 PnL:
{pnl_percent:.2f}%

🤖 Trade closed automatically
"""

                    send_telegram_message(message)

                    print(f"❌ {symbol} SL HIT")

                    continue

                # ======================================
                # TAKE PROFIT HIT
                # ======================================

                if current_price >= take_profit:

                    close_trade(trade_id, current_price, close_reason="TAKE PROFIT")

                    message = f"""
✅ <b>TAKE PROFIT HIT</b>

🚀 {symbol}

💰 Buy: {buy_price:.2f}
💵 Sell: {current_price:.2f}

📊 PnL:
+{pnl_percent:.2f}%

🤖 Trade closed automatically
"""

                    send_telegram_message(message)

                    print(f"✅ {symbol} TP HIT")

                    continue

                # ======================================
                # TRAILING INFO
                # ======================================

                print(f"⏳ {symbol} still open")

            except Exception as e:

                print(f"❌ Trade Audit Error " f"{trade.get('symbol')}: " f"{e}")

    except Exception as e:

        print(f"❌ Audit Engine Error: {e}")
