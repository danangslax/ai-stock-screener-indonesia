import json

from datetime import datetime

from pathlib import Path

from infrastructure.logger import logger

# ======================================
# JOURNAL FILE
# ======================================

JOURNAL_PATH = Path("data") / "trades" / "trade_journal.json"

# ======================================
# LOAD JOURNAL
# ======================================


def load_journal():

    try:

        if not JOURNAL_PATH.exists():

            return []

        with open(JOURNAL_PATH, "r", encoding="utf-8") as f:

            data = json.load(f)

        if not isinstance(data, list):

            logger.warning("Invalid journal format")

            return []

        return data

    except Exception as e:

        logger.error(f"Load journal error: " f"{e}")

        return []


# ======================================
# SAVE JOURNAL
# ======================================


def save_journal(data):

    try:

        # ======================================
        # CREATE DIRECTORY
        # ======================================

        JOURNAL_PATH.parent.mkdir(parents=True, exist_ok=True)

        # ======================================
        # TEMP FILE
        # ======================================

        temp_path = JOURNAL_PATH.with_suffix(".tmp")

        # ======================================
        # SAVE TEMP
        # ======================================

        with open(temp_path, "w", encoding="utf-8") as f:

            json.dump(data, f, indent=4, ensure_ascii=False)

        # ======================================
        # ATOMIC REPLACE
        # ======================================

        temp_path.replace(JOURNAL_PATH)

        logger.info("Trade journal saved")

        return True

    except Exception as e:

        logger.error(f"Save journal error: " f"{e}")

        return False


# ======================================
# ADD JOURNAL ENTRY
# ======================================


def add_trade_journal(
    symbol,
    strategy,
    market_regime,
    confidence,
    entry_reason,
    emotion="NEUTRAL",
    result="OPEN",
    lesson="",
    stop_loss=None,
    take_profit=None,
    risk_reward=None,
):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if not symbol:

            raise ValueError("Invalid symbol")

        journal = load_journal()

        # ======================================
        # TRADE ID
        # ======================================

        trade_id = f"{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # ======================================
        # JOURNAL ENTRY
        # ======================================

        entry = {
            "trade_id": (trade_id),
            "created_at": (datetime.now().isoformat()),
            "symbol": (symbol),
            "strategy": (strategy),
            "market_regime": (market_regime),
            "confidence": (confidence),
            "entry_reason": (entry_reason),
            "emotion": (emotion),
            "result": (result),
            "lesson": (lesson),
            "stop_loss": (stop_loss),
            "take_profit": (take_profit),
            "risk_reward": (risk_reward),
            "status": "OPEN",
        }

        # ======================================
        # SAVE
        # ======================================

        journal.append(entry)

        save_journal(journal)

        logger.info(f"Journal saved | " f"{symbol}")

        return trade_id

    except Exception as e:

        logger.error(f"Journal error: " f"{e}")

        return None


# ======================================
# UPDATE TRADE RESULT
# ======================================


def update_trade_result(
    trade_id,
    result,
    lesson="",
    emotion=None,
    profit_loss=None,
):

    try:

        journal = load_journal()

        updated = False

        # ======================================
        # LOOP JOURNAL
        # ======================================

        for trade in journal:

            if trade.get("trade_id") == trade_id:

                trade["result"] = result

                trade["lesson"] = lesson

                trade["status"] = "CLOSED"

                trade["updated_at"] = datetime.now().isoformat()

                if emotion:

                    trade["emotion"] = emotion

                if profit_loss is not None:

                    trade["profit_loss"] = round(profit_loss, 2)

                updated = True

                break

        # ======================================
        # SAVE
        # ======================================

        if updated:

            save_journal(journal)

            logger.info(f"Journal updated | " f"{trade_id}")

            return True

        logger.warning(f"Trade ID not found | " f"{trade_id}")

        return False

    except Exception as e:

        logger.error(f"Update journal error: " f"{e}")

        return False
