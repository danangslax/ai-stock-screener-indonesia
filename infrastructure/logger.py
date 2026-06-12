import logging

from pathlib import Path

# ======================================
# LOG DIRECTORY
# ======================================

LOG_DIR = Path("logs")

LOG_DIR.mkdir(parents=True, exist_ok=True)

# ======================================
# LOG FILE
# ======================================

LOG_FILE = LOG_DIR / "system.log"

# ======================================
# LOGGER
# ======================================

logger = logging.getLogger("AI_STOCK_SCREENER")

# ======================================
# PREVENT DUPLICATE HANDLER
# ======================================

if not logger.handlers:

    logger.setLevel(logging.INFO)

    # ======================================
    # FORMATTER
    # ======================================

    formatter = logging.Formatter("%(asctime)s | " "%(levelname)s | " "%(message)s")

    # ======================================
    # FILE HANDLER
    # ======================================

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")

    file_handler.setFormatter(formatter)

    # ======================================
    # STREAM HANDLER
    # ======================================

    stream_handler = logging.StreamHandler()

    stream_handler.setFormatter(formatter)

    # ======================================
    # ADD HANDLERS
    # ======================================

    logger.addHandler(file_handler)

    logger.addHandler(stream_handler)
