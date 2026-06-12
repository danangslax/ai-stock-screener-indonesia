from pathlib import Path

import pandas as pd

# ======================================
# CACHE DIRECTORY
# ======================================

CACHE_DIR = Path("data") / "cache"

# ======================================
# VALIDATE CACHE FILE
# ======================================


def validate_cache_file(file_path):

    try:

        df = pd.read_parquet(file_path)

        # ======================================
        # EMPTY
        # ======================================

        if df.empty:

            return False

        # ======================================
        # REQUIRED COLUMNS
        # ======================================

        required_columns = [
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

        missing = [col for col in required_columns if col not in df.columns]

        if missing:

            print(f"⚠️ Missing columns: " f"{missing}")

            return False

        # ======================================
        # MINIMUM DATA
        # ======================================

        if len(df) < 50:

            return False

        return True

    except Exception as e:

        print(f"❌ Validation error: " f"{e}")

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

        print(f"📦 Total cache files: " f"{total}")

        for file in files:

            result = validate_cache_file(file)

            if result:

                valid.append(file.name)

            else:

                invalid.append(file.name)

        summary = {
            "total": total,
            "valid": len(valid),
            "invalid": len(invalid),
            "invalid_files": invalid,
        }

        return summary

    except Exception as e:

        print(f"❌ Cache validation error: " f"{e}")

        return {}
