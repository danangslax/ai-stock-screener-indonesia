import json

from pathlib import Path

# ======================================
# JOURNAL FILE
# ======================================

JOURNAL_PATH = Path("data") / "trade_journal.json"

# ======================================
# LOAD JOURNAL
# ======================================


def load_journal():

    try:

        if not JOURNAL_PATH.exists():

            return []

        with open(JOURNAL_PATH, "r", encoding="utf-8") as f:

            return json.load(f)

    except Exception as e:

        print(f"❌ Load journal error: " f"{e}")

        return []


# ======================================
# SAVE JOURNAL
# ======================================


def save_journal(data):

    try:

        JOURNAL_PATH.parent.mkdir(parents=True, exist_ok=True)

        with open(JOURNAL_PATH, "w", encoding="utf-8") as f:

            json.dump(data, f, indent=4)

    except Exception as e:

        print(f"❌ Save journal error: " f"{e}")


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
):

    try:

        journal = load_journal()

        entry = {
            "symbol": symbol,
            "strategy": strategy,
            "market_regime": market_regime,
            "confidence": confidence,
            "entry_reason": entry_reason,
            "emotion": emotion,
            "result": result,
            "lesson": lesson,
        }

        journal.append(entry)

        save_journal(journal)

        print(f"✅ Journal saved: " f"{symbol}")

        return True

    except Exception as e:

        print(f"❌ Journal error: " f"{e}")

        return False


# ======================================
# UPDATE TRADE RESULT
# ======================================


def update_trade_result(symbol, result, lesson=""):

    try:

        journal = load_journal()

        for trade in journal:

            if trade["symbol"] == symbol:

                trade["result"] = result

                trade["lesson"] = lesson

        save_journal(journal)

        return True

    except Exception as e:

        print(f"❌ Update journal error: " f"{e}")

        return False
