from database.db import supabase

# ======================================
# CREATE PAPER TRADE
# ======================================


def create_trade(symbol, buy_price, quantity, strategy="UNKNOWN"):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if buy_price <= 0:

            raise ValueError("Invalid buy price")

        if quantity <= 0:

            raise ValueError("Invalid quantity")

        # ======================================
        # CHECK DUPLICATE OPEN TRADE
        # ======================================

        existing = (
            supabase.table("paper_trades")
            .select("*")
            .eq("symbol", symbol)
            .eq("status", "OPEN")
            .execute()
        )

        if existing.data:

            print(f"⚠️ Open trade already exists " f"for {symbol}")

            return None

        # ======================================
        # DEFAULT RISK MANAGEMENT
        # ======================================

        if stop_loss is None:

            stop_loss = round(buy_price * 0.95, 2)

        if take_profit is None:

            take_profit = round(buy_price * 1.10, 2)

        # ======================================
        # TRADE DATA
        # ======================================

        data = {
            "symbol": symbol,
            "buy_price": round(buy_price, 2),
            "quantity": quantity,
            "status": "OPEN",
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "profit_loss": 0,
            "close_reason": None,
            "strategy": strategy,
            "market_regime": market_regime,
            "position_value": (buy_price * quantity),
        }

        # ======================================
        # INSERT DATABASE
        # ======================================

        response = supabase.table("paper_trades").insert(data).execute()

        print(f"✅ Trade created: {symbol}")

        return response

    except Exception as e:

        print(f"❌ Create Trade Error: {e}")

        return None


# ======================================
# CLOSE TRADE
# ======================================


def close_trade(trade_id, sell_price, close_reason="MANUAL"):

    try:

        # ======================================
        # LOAD TRADE
        # ======================================

        trade = supabase.table("paper_trades").select("*").eq("id", trade_id).execute()

        if not trade.data:

            print("❌ Trade not found")

            return None

        trade_data = trade.data[0]

        # ======================================
        # VALIDATION
        # ======================================

        if trade_data["status"] == "CLOSED":

            print("⚠️ Trade already closed")

            return None

        # ======================================
        # CALCULATE PNL
        # ======================================

        buy_price = float(trade_data["buy_price"])

        quantity = int(trade_data["quantity"])

        pnl = (sell_price - buy_price) * quantity

        pnl_percent = ((sell_price - buy_price) / buy_price) * 100

        # ======================================
        # WIN / LOSS
        # ======================================

        if pnl > 0:

            result = "WIN"

        elif pnl < 0:

            result = "LOSS"

        else:

            result = "BREAKEVEN"

        # ======================================
        # UPDATE DATABASE
        # ======================================

        response = (
            supabase.table("paper_trades")
            .update(
                {
                    "sell_price": round(sell_price, 2),
                    "profit_loss": round(pnl, 2),
                    "profit_loss_percent": round(pnl_percent, 2),
                    "status": "CLOSED",
                    "result": result,
                    "close_reason": close_reason,
                }
            )
            .eq("id", trade_id)
            .execute()
        )

        print(f"✅ Trade closed: " f"{trade_data['symbol']}")

        return response

    except Exception as e:

        print(f"❌ Close Trade Error: {e}")

        return None


# ======================================
# LOAD ALL TRADES
# ======================================


def load_trades():

    try:

        response = (
            supabase.table("paper_trades")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

        return response.data

    except Exception as e:

        print(f"❌ Load Trades Error: {e}")

        return []


# ======================================
# LOAD OPEN TRADES
# ======================================


def load_open_trades():

    try:

        response = (
            supabase.table("paper_trades")
            .select("*")
            .eq("status", "OPEN")
            .order("created_at", desc=True)
            .execute()
        )

        return response.data

    except Exception as e:

        print(f"❌ Load Open Trades Error: {e}")

        return []


# ======================================
# LOAD CLOSED TRADES
# ======================================


def load_closed_trades():

    try:

        response = (
            supabase.table("paper_trades")
            .select("*")
            .eq("status", "CLOSED")
            .order("created_at", desc=True)
            .execute()
        )

        return response.data

    except Exception as e:

        print(f"❌ Load Closed Trades Error: {e}")

        return []
