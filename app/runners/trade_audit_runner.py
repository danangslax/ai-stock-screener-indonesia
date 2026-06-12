import time

from analytics.trade_audit import run_trade_audit

from infrastructure.notifier import send_telegram_message

from infrastructure.logger import logger

from infrastructure.audit import audit_event

from infrastructure.recovery import safe_execute

from market.market import get_market_status

from trading.paper_trading import load_open_trades

# ======================================
# TRADE AUDIT RUNNER
# ======================================


def main():

    try:

        start_time = time.time()

        logger.info("TRADE AUDIT STARTED")

        audit_event("TRADE_AUDIT_START", "Portfolio surveillance engine")

        # ======================================
        # MARKET STATUS
        # ======================================

        market = safe_execute(get_market_status)

        market_status = "UNKNOWN"

        if market:

            market_status = market.get("status", "UNKNOWN")

        logger.info(f"Market Status: " f"{market_status}")

        # ======================================
        # LOAD OPEN TRADES
        # ======================================

        open_trades = safe_execute(load_open_trades)

        if open_trades is None:

            open_trades = []

        total_open = len(open_trades)

        logger.info(f"Open Trades: " f"{total_open}")

        # ======================================
        # NO OPEN TRADES
        # ======================================

        if total_open == 0:

            message = f"""
📊 <b>TRADE AUDIT</b>

⚠️ No open trades found.

🌍 Market:
<b>{market_status}</b>

🤖 Audit Engine
"""

            safe_execute(send_telegram_message, message)

            logger.warning("No open trades found")

            audit_event("NO_OPEN_TRADES", market_status)

            return

        # ======================================
        # TRADE EXPOSURE
        # ======================================

        total_exposure = 0

        for trade in open_trades:

            try:

                total_exposure += float(trade.get("position_value", 0))

            except:

                pass

        logger.info(f"Total Exposure: " f"{round(total_exposure, 2)}")

        # ======================================
        # MARKET RISK WARNING
        # ======================================

        dangerous_market = ["PANIC", "BEARISH"]

        if market_status in dangerous_market:

            warning_message = f"""
⚠️ <b>MARKET RISK WARNING</b>

🌍 Current Market:
<b>{market_status}</b>

📂 Open Trades:
{total_open}

💰 Exposure:
{round(total_exposure, 2)}

⚠️ Defensive monitoring active.

🤖 Risk Engine
"""

            safe_execute(send_telegram_message, warning_message)

        # ======================================
        # RUN AUDIT ENGINE
        # ======================================

        safe_execute(run_trade_audit)

        # ======================================
        # EXECUTION TIME
        # ======================================

        execution_time = round(time.time() - start_time, 2)

        # ======================================
        # HEALTH STATUS
        # ======================================

        health_status = "HEALTHY"

        if total_open >= 10:

            health_status = "HIGH_EXPOSURE"

        if market_status in dangerous_market:

            health_status = "DEFENSIVE"

        # ======================================
        # SUMMARY
        # ======================================

        summary_message = f"""
📊 <b>TRADE AUDIT COMPLETE</b>

✅ Open Trades Checked:
{total_open}

💰 Total Exposure:
{round(total_exposure, 2)}

🌍 Market:
<b>{market_status}</b>

🛡 Risk Status:
<b>{health_status}</b>

⏱ Execution:
{execution_time}s

🤖 AI Trade Surveillance
"""

        safe_execute(send_telegram_message, summary_message)

        # ======================================
        # FINAL LOG
        # ======================================

        logger.info("=================================")

        logger.info("TRADE AUDIT COMPLETE")

        logger.info(f"Open Trades: " f"{total_open}")

        logger.info(f"Exposure: " f"{round(total_exposure, 2)}")

        logger.info(f"Risk Status: " f"{health_status}")

        logger.info(f"Execution Time: " f"{execution_time}s")

        logger.info("=================================")

        audit_event(
            "TRADE_AUDIT_COMPLETE",
            f"Trades={total_open} | " f"Exposure={round(total_exposure, 2)}",
        )

    except Exception as e:

        logger.error(f"Trade Audit Runner Error: {e}")

        safe_execute(send_telegram_message, f"❌ Trade Audit Error:\n{e}")


# ======================================
# ENTRY POINT
# ======================================

if __name__ == "__main__":

    main()
