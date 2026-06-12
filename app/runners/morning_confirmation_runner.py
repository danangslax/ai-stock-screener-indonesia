import time

from strategies.confirmation import morning_confirmation

from market.market import get_market_status

from infrastructure.logger import logger

from infrastructure.audit import audit_event

from infrastructure.recovery import safe_execute

from infrastructure.notifier import send_telegram_message, format_confirmation_message

from database.queries import load_screener_history

# ======================================
# MORNING CONFIRMATION RUNNER
# ======================================


def main():

    try:

        start_time = time.time()

        logger.info("MORNING CONFIRMATION STARTED")

        audit_event("MORNING_CONFIRMATION_START", "Morning validation engine")

        # ======================================
        # MARKET STATUS
        # ======================================

        market = safe_execute(get_market_status)

        if not market:

            logger.error("Failed to get market status")

            return

        market_status = market.get("status", "UNKNOWN")

        logger.info(f"Market Status: " f"{market_status}")

        # ======================================
        # MARKET PROTECTION
        # ======================================

        dangerous_market = ["PANIC", "BEARISH"]

        if market_status in dangerous_market:

            warning_message = f"""
⚠️ <b>MARKET WARNING</b>

🌍 Current Market:
<b>{market_status}</b>

Morning confirmation running
under defensive mode.

🤖 AI Risk Engine
"""

            send_telegram_message(warning_message)

        # ======================================
        # LOAD HISTORY
        # ======================================

        history = safe_execute(load_screener_history, limit=10)

        if not history:

            logger.warning("No screener history found")

            send_telegram_message("⚠️ No screener history found")

            return

        # ======================================
        # STATISTICS
        # ======================================

        total_processed = 0

        strong_buy_count = 0

        buy_count = 0

        watch_count = 0

        weak_count = 0

        avoid_count = 0

        error_count = 0

        # ======================================
        # PROCESS STOCKS
        # ======================================

        for stock in history:

            try:

                symbol = stock["Symbol"]

                logger.info(f"Confirming {symbol}")

                # ======================================
                # CONFIRMATION ENGINE
                # ======================================

                confirmation = safe_execute(morning_confirmation, symbol)

                if not confirmation:

                    confirmation = "ERROR"

                # ======================================
                # STATISTICS
                # ======================================

                if confirmation == "STRONG BUY":

                    strong_buy_count += 1

                elif confirmation == "BUY":

                    buy_count += 1

                elif confirmation == "WATCH":

                    watch_count += 1

                elif confirmation == "WEAK":

                    weak_count += 1

                elif confirmation == "AVOID":

                    avoid_count += 1

                else:

                    error_count += 1

                # ======================================
                # FORMAT MESSAGE
                # ======================================

                message = format_confirmation_message(symbol, confirmation)

                # ======================================
                # MARKET INFO
                # ======================================

                message += f"""

🌍 Market:
<b>{market_status}</b>

🤖 AI Confirmation Engine
"""

                # ======================================
                # SEND TELEGRAM
                # ======================================

                safe_execute(send_telegram_message, message)

                logger.info(f"{symbol}: " f"{confirmation}")

                audit_event("MORNING_CONFIRMATION", f"{symbol} | " f"{confirmation}")

                total_processed += 1

            except Exception as stock_error:

                logger.error(
                    f"Confirmation Error " f"{stock.get('Symbol')}: " f"{stock_error}"
                )

                error_count += 1

        # ======================================
        # EXECUTION TIME
        # ======================================

        execution_time = round(time.time() - start_time, 2)

        # ======================================
        # SUMMARY MESSAGE
        # ======================================

        summary_message = f"""
☀️ <b>MORNING CONFIRMATION COMPLETE</b>

📊 Processed:
{total_processed}

🚀 Strong Buy:
{strong_buy_count}

✅ Buy:
{buy_count}

👀 Watch:
{watch_count}

⚠️ Weak:
{weak_count}

❌ Avoid:
{avoid_count}

🔥 Errors:
{error_count}

🌍 Market:
<b>{market_status}</b>

⏱ Execution:
{execution_time}s

🤖 AI Confirmation Engine
"""

        safe_execute(send_telegram_message, summary_message)

        # ======================================
        # FINAL LOG
        # ======================================

        logger.info("=================================")

        logger.info("MORNING CONFIRMATION COMPLETE")

        logger.info(f"Processed: " f"{total_processed}")

        logger.info(f"Strong Buy: " f"{strong_buy_count}")

        logger.info(f"Buy: " f"{buy_count}")

        logger.info(f"Avoid: " f"{avoid_count}")

        logger.info(f"Execution Time: " f"{execution_time}s")

        logger.info("=================================")

        audit_event("MORNING_CONFIRMATION_COMPLETE", f"Processed={total_processed}")

    except Exception as e:

        logger.error(f"Morning Runner Error: {e}")

        safe_execute(send_telegram_message, f"❌ Morning Confirmation Error:\n{e}")


# ======================================
# ENTRY POINT
# ======================================

if __name__ == "__main__":

    main()
