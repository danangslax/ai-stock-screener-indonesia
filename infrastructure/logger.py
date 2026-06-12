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
# LOGGER CONFIG
# ======================================

logging.basicConfig(
    level=logging.INFO,
    format=("%(asctime)s | " "%(levelname)s | " "%(message)s"),
    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8"), logging.StreamHandler()],
)

# ======================================
# LOGGER
# ======================================

logger = logging.getLogger("AI_STOCK_SCREENER")
