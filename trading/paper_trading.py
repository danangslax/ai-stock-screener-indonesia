from datetime import datetime

from database.db import supabase

from infrastructure.logger import logger

# ======================================
# CREATE PAPER TRADE
# ======================================


def create_trade(
    symbol,
    buy_price,
    quantity,
    strategy="UNKNOWN",
    market_regime="UNKNOWN",
    stop_loss=None,
    take_profit=None,
):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if not symbol:

            raise ValueError("Invalid symbol")

        if buy_price <= 0:

            raise ValueError("Invalid buy price")

        if quantity <= 0:

            raise ValueError("Invalid quantity")

        # ======================================
        # POSITION VALUE
        # ======================================

        position_value = buy_price * quantity

        # ======================================
        # MAX POSITION LIMIT
        # ======================================

        max_position_value = 50_000_000

        if position_value > max_position_value:

            raise ValueError(f"Position too large: " f"{position_value}")

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

            logger.warning(f"Open trade already " f"exists for {symbol}")

            return None

        # ======================================
        # DEFAULT RISK MANAGEMENT
        # ======================================

        if stop_loss is None:

            stop_loss = round(buy_price * 0.95, 2)

        if take_profit is None:

            take_profit = round(buy_price * 1.10, 2)

        # ======================================
        # VALIDATE RISK
        # ======================================

        if stop_loss >= buy_price:

            raise ValueError("Invalid stop loss")

        if take_profit <= buy_price:

            raise ValueError("Invalid take profit")

        # ======================================
        # RISK REWARD
        # ======================================

        risk = buy_price - stop_loss

        reward = take_profit - buy_price

        rr_ratio = 0

        if risk > 0:

            rr_ratio = round(reward / risk, 2)

        # ======================================
        # TRADE DATA
        # ======================================

        data = {
            "symbol": (symbol),
            "buy_price": round(buy_price, 2),
            "quantity": (quantity),
            "status": "OPEN",
            "stop_loss": (stop_loss),
            "take_profit": (take_profit),
            "profit_loss": 0,
            "profit_loss_percent": 0,
            "close_reason": None,
            "strategy": (strategy),
            "market_regime": (market_regime),
            "position_value": round(position_value, 2),
            "risk_reward": (rr_ratio),
            "created_at": (datetime.now().isoformat()),
        }

        # ======================================
        # INSERT DATABASE
        # ======================================

        response = supabase.table("paper_trades").insert(data).execute()

        logger.info(f"Trade created | " f"{symbol} | " f"Strategy={strategy}")

        return response

    except Exception as e:

        logger.error(f"Create Trade Error: " f"{e}")

        return None


# ======================================
# CLOSE TRADE
# ======================================


def close_trade(trade_id, sell_price, close_reason="MANUAL"):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if sell_price <= 0:

            raise ValueError("Invalid sell price")

        # ======================================
        # LOAD TRADE
        # ======================================

        trade = supabase.table("paper_trades").select("*").eq("id", trade_id).execute()

        if not trade.data:

            logger.warning("Trade not found")

            return None

        trade_data = trade.data[0]

        # ======================================
        # ALREADY CLOSED
        # ======================================

        if trade_data["status"] == "CLOSED":

            logger.warning("Trade already closed")

            return None

        # ======================================
        # CALCULATE PNL
        # ======================================

        buy_price = float(trade_data["buy_price"])

        quantity = int(trade_data["quantity"])

        pnl = (sell_price - buy_price) * quantity

        pnl_percent = round(((sell_price - buy_price) / buy_price) * 100, 2)

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
                    "profit_loss_percent": (pnl_percent),
                    "status": "CLOSED",
                    "result": result,
                    "close_reason": (close_reason),
                    "closed_at": (datetime.now().isoformat()),
                }
            )
            .eq("id", trade_id)
            .execute()
        )

        logger.info(
            f"Trade closed | " f"{trade_data['symbol']} | " f"PnL={round(pnl,2)}"
        )

        return response

    except Exception as e:

        logger.error(f"Close Trade Error: " f"{e}")

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

        logger.error(f"Load Trades Error: " f"{e}")

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

        logger.error(f"Load Open Trades Error: " f"{e}")

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

        logger.error(f"Load Closed Trades Error: " f"{e}")

        return []
