from database.db import supabase

# ======================================
# CREATE PAPER TRADE
# ======================================

def create_trade(
    symbol,
    buy_price,
    quantity=1
):

    stop_loss = buy_price * 0.95
    take_profit = buy_price * 1.10

    data = {
        "symbol": symbol,
        "buy_price": buy_price,
        "quantity": quantity,
        "status": "OPEN",
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "profit_loss": 0
    }

    response = supabase.table(
        "paper_trades"
    ).insert(data).execute()

    return response

# ======================================
# CLOSE TRADE
# ======================================

def close_trade(
    trade_id,
    sell_price
):

    trade = supabase.table(
        "paper_trades"
    ).select("*").eq(
        "id",
        trade_id
    ).execute()

    if not trade.data:
        return

    trade_data = trade.data[0]

    buy_price = float(
        trade_data["buy_price"]
    )

    quantity = int(
        trade_data["quantity"]
    )

    pnl = (
        sell_price - buy_price
    ) * quantity

    response = supabase.table(
        "paper_trades"
    ).update({
        "sell_price": sell_price,
        "profit_loss": pnl,
        "status": "CLOSED"
    }).eq(
        "id",
        trade_id
    ).execute()

    return response

# ======================================
# LOAD TRADES
# ======================================

def load_trades():

    response = supabase.table(
        "paper_trades"
    ).select("*").order(
        "created_at",
        desc=True
    ).execute()

    return response.data

