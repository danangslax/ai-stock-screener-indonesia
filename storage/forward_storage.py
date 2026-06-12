import json

from pathlib import Path

from datetime import datetime

from infrastructure.logger import logger

# ======================================
# FORWARD DIRECTORY
# ======================================

FORWARD_DIR = Path("data") / "forward"

FORWARD_DIR.mkdir(parents=True, exist_ok=True)

# ======================================
# FORWARD SIGNAL FILE
# ======================================

FORWARD_PATH = FORWARD_DIR / "forward_signals.json"

# ======================================
# LOAD SIGNALS
# ======================================


def load_forward_signals():

    try:

        # ======================================
        # FILE EXISTS
        # ======================================

        if not FORWARD_PATH.exists():

            logger.warning("Forward signals not found")

            return []

        # ======================================
        # LOAD JSON
        # ======================================

        with open(FORWARD_PATH, "r", encoding="utf-8") as f:

            signals = json.load(f)

        # ======================================
        # VALIDATION
        # ======================================

        if not isinstance(signals, list):

            logger.warning("Invalid forward signal format")

            return []

        return signals

    except Exception as e:

        logger.error(f"Load forward error: " f"{e}")

        return []


# ======================================
# SAVE SIGNALS
# ======================================


def save_forward_signals(data):

    try:

        # ======================================
        # TEMP FILE
        # ======================================

        temp_path = FORWARD_PATH.with_suffix(".tmp")

        # ======================================
        # SAVE TEMP
        # ======================================

        with open(temp_path, "w", encoding="utf-8") as f:

            json.dump(data, f, indent=4, ensure_ascii=False)

        # ======================================
        # REPLACE FILE
        # ======================================

        temp_path.replace(FORWARD_PATH)

        logger.info("Forward signals saved")

    except Exception as e:

        logger.error(f"Save forward error: " f"{e}")


# ======================================
# ADD SIGNAL
# ======================================


def add_forward_signal(signal):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if not isinstance(signal, dict):

            logger.warning("Invalid signal format")

            return False

        # ======================================
        # REQUIRED FIELDS
        # ======================================

        required_fields = ["Symbol", "Price", "Score"]

        missing = [field for field in required_fields if field not in signal]

        if missing:

            logger.warning(f"Missing signal fields: " f"{missing}")

            return False

        # ======================================
        # LOAD SIGNALS
        # ======================================

        signals = load_forward_signals()

        # ======================================
        # TIMESTAMP
        # ======================================

        signal["created_at"] = str(datetime.now())

        # ======================================
        # DUPLICATE CHECK
        # ======================================

        duplicate = any(
            s.get("Symbol") == signal.get("Symbol")
            and s.get("created_at", "")[:10] == signal["created_at"][:10]
            for s in signals
        )

        if duplicate:

            logger.warning(f"Duplicate signal: " f"{signal['Symbol']}")

            return False

        # ======================================
        # APPEND SIGNAL
        # ======================================

        signals.append(signal)

        # ======================================
        # SAVE
        # ======================================

        save_forward_signals(signals)

        logger.info(f"Forward signal added: " f"{signal['Symbol']}")

        return True

    except Exception as e:

        logger.error(f"Add forward error: " f"{e}")

        return False
