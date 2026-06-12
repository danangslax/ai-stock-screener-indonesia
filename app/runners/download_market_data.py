import time
import yfinance as yf
import pandas as pd

from pathlib import Path

from storage.indicators import add_indicators

# ======================================
# LOAD WATCHLIST
# ======================================

WATCHLIST_PATH = Path("watchlist") / "idx_stocks.txt"

with open(WATCHLIST_PATH, "r", encoding="utf-8") as f:

    IDX_STOCKS = [line.strip() for line in f if line.strip()]

# ======================================
# CACHE DIRECTORY
# ======================================

CACHE_DIR = Path("data") / "cache"

CACHE_DIR.mkdir(parents=True, exist_ok=True)

# ======================================
# REQUIRED COLUMNS
# ======================================

REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]

# ======================================
# DOWNLOAD STOCK DATA
# ======================================


def download_stock(symbol):

    try:

        print(f"⬇️ Downloading {symbol}")

        # ======================================
        # DOWNLOAD DATA
        # ======================================

        df = yf.download(
            symbol,
            period="1y",
            interval="1d",
            auto_adjust=True,
            progress=False,
            threads=False,
        )

        # ======================================
        # FIX MULTI INDEX
        # ======================================

        if isinstance(df.columns, pd.MultiIndex):

            df.columns = df.columns.get_level_values(0)

        # ======================================
        # VALIDATION
        # ======================================

        if df.empty:

            print(f"⚠️ Empty data: " f"{symbol}")

            return False

        # ======================================
        # REQUIRED COLUMNS CHECK
        # ======================================

        missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]

        if missing_columns:

            print(f"⚠️ Missing columns " f"{symbol}: " f"{missing_columns}")

            return False

        # ======================================
        # CLEAN DATA
        # ======================================

        df = df.copy()

        df = df.sort_index()

        df = df[~df.index.duplicated()]

        # ======================================
        # ADD INDICATORS
        # ======================================

        df = add_indicators(df)

        if df.empty:

            print(f"⚠️ Indicator failed: " f"{symbol}")

            return False

        # ======================================
        # FINAL VALIDATION
        # ======================================

        if "RSI" not in df.columns:

            print(f"⚠️ Indicator incomplete: " f"{symbol}")

            return False

        # ======================================
        # FILE PATH
        # ======================================

        file_path = CACHE_DIR / f"{symbol}.parquet"

        # ======================================
        # SAVE ENRICHED CACHE
        # ======================================

        df.to_parquet(file_path, index=True)

        print(f"✅ Saved enriched cache: " f"{symbol}")

        return True

    except Exception as e:

        print(f"❌ Download Error " f"{symbol}: {e}")

        return False


# ======================================
# MAIN ENGINE
# ======================================


def main():

    print("")
    print("=================================")

    print("🚀 DOWNLOADING MARKET DATA")

    print("=================================")

    success = 0

    failed = 0

    total = len(IDX_STOCKS)

    # ======================================
    # LOOP STOCKS
    # ======================================

    for i, symbol in enumerate(IDX_STOCKS):

        print("")
        print(f"📊 {i+1}/{total}")

        result = download_stock(symbol)

        if result:

            success += 1

        else:

            failed += 1

        # ======================================
        # ANTI RATE LIMIT
        # ======================================

        time.sleep(1)

    # ======================================
    # SUMMARY
    # ======================================

    print("")
    print("=================================")

    print("✅ DOWNLOAD COMPLETE")

    print(f"Success: {success}")

    print(f"Failed: {failed}")

    print("=================================")


# ======================================
# ENTRY POINT
# ======================================

if __name__ == "__main__":

    main()
