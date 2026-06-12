from pathlib import Path

import pandas as pd

from infrastructure.logger import logger

# ======================================
# CACHE DIRECTORY
# ======================================

CACHE_DIR = Path("data") / "cache"

CACHE_DIR.mkdir(parents=True, exist_ok=True)

# ======================================
# REQUIRED COLUMNS
# ======================================

REQUIRED_COLUMNS = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
    "RSI",
    "ADX",
    "ATR",
    "EMA20",
    "EMA50",
]

# ======================================
# VALIDATE CACHE FILE
# ======================================


def validate_cache_file(file_path):

    try:

        df = pd.read_parquet(file_path)

        # ======================================
        # EMPTY CHECK
        # ======================================

        if df.empty:

            logger.warning(f"[CACHE] Empty file: " f"{file_path.name}")

            return False

        # ======================================
        # REQUIRED COLUMNS
        # ======================================

        missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]

        if missing:

            logger.warning(
                f"[CACHE] Missing columns " f"{file_path.name}: " f"{missing}"
            )

            return False

        # ======================================
        # MINIMUM DATA
        # ======================================

        if len(df) < 50:

            logger.warning(f"[CACHE] Insufficient rows: " f"{file_path.name}")

            return False

        return True

    except Exception as e:

        logger.error(f"[CACHE] Validation failed: " f"{file_path.name} | " f"{e}")

        return False


# ======================================
# VALIDATE ALL CACHE
# ======================================


def validate_all_cache():

    try:

        files = list(CACHE_DIR.glob("*.parquet"))

        valid = []

        invalid = []

        total = len(files)

        logger.info(f"[CACHE] Total files: " f"{total}")

        # ======================================
        # LOOP FILES
        # ======================================

        for file in files:

            result = validate_cache_file(file)

            if result:

                valid.append(file.name)

            else:

                invalid.append(file.name)

        # ======================================
        # VALIDATION RATE
        # ======================================

        validation_rate = 0

        if total > 0:

            validation_rate = round((len(valid) / total) * 100, 2)

        # ======================================
        # SUMMARY
        # ======================================

        summary = {
            "total": total,
            "valid": len(valid),
            "invalid": len(invalid),
            "validation_rate": validation_rate,
            "valid_files": valid,
            "invalid_files": invalid,
        }

        logger.info(
            f"[CACHE] Validation "
            f"completed | "
            f"Valid={len(valid)} | "
            f"Invalid={len(invalid)}"
        )

        return summary

    except Exception as e:

        logger.error(f"[CACHE] Validation " f"system failed: {e}")

        return {}
