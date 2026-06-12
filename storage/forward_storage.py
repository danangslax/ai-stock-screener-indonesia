import json

from pathlib import Path

# ======================================
# FORWARD SIGNAL FILE
# ======================================

FORWARD_PATH = Path("data") / "forward_signals.json"

# ======================================
# LOAD SIGNALS
# ======================================


def load_forward_signals():

    try:

        if not FORWARD_PATH.exists():

            return []

        with open(FORWARD_PATH, "r", encoding="utf-8") as f:

            return json.load(f)

    except Exception as e:

        print(f"❌ Load forward error: " f"{e}")

        return []


# ======================================
# SAVE SIGNALS
# ======================================


def save_forward_signals(data):

    try:

        FORWARD_PATH.parent.mkdir(parents=True, exist_ok=True)

        with open(FORWARD_PATH, "w", encoding="utf-8") as f:

            json.dump(data, f, indent=4)

    except Exception as e:

        print(f"❌ Save forward error: " f"{e}")


# ======================================
# ADD SIGNAL
# ======================================


def add_forward_signal(signal):

    try:

        signals = load_forward_signals()

        signals.append(signal)

        save_forward_signals(signals)

        return True

    except Exception as e:

        print(f"❌ Add forward error: " f"{e}")

        return False
