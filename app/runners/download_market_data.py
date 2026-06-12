import time
import yfinance as yf
import pandas as pd

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from storage.indicators import add_indicators

from infrastructure.logger import logger

from infrastructure.audit import audit_event

from infrastructure.recovery import safe_execute

# ======================================
# WATCHLIST
# ======================================

WATCHLIST_PATH = Path("watchlist") / "idx_stocks.txt"

with open(
    WATCHLIST_PATH,
    "r",
    encoding="utf-8",
) as f:

    IDX_STOCKS = [line.strip() for line in f if line.strip()]

# ======================================
# ADD MARKET BENCHMARK
# ======================================

if "^JKSE" not in IDX_STOCKS:

    IDX_STOCKS.append("^JKSE")

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
]

# ======================================
# DOWNLOAD STOCK
# ======================================


def download_stock(symbol):

    try:

        logger.info(f"Downloading {symbol}")

        cache_path = CACHE_DIR / f"{symbol}.parquet"

        # ======================================
        # CACHE FRESHNESS CHECK
        # ======================================

        if cache_path.exists():

            modified_time = cache_path.stat().st_mtime

            current_time = time.time()

            # Skip if updated < 12 hours
            if (current_time - modified_time) < (60 * 60 * 12):

                logger.info(f"Fresh cache skip: {symbol}")

                return True

        # ======================================
        # RETRY SYSTEM
        # ======================================

        max_retries = 3

        for attempt in range(max_retries):

            try:

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

                    logger.warning(f"Empty data: {symbol}")

                    continue

                # ======================================
                # REQUIRED COLUMNS
                # ======================================

                missing_columns = [
                    col for col in REQUIRED_COLUMNS if col not in df.columns
                ]

                if missing_columns:

                    logger.warning(
                        f"Missing columns " f"{symbol}: " f"{missing_columns}"
                    )

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

                    logger.warning(f"Indicator failed: " f"{symbol}")

                    continue

                # ======================================
                # FINAL VALIDATION
                # ======================================

                if "RSI" not in df.columns:

                    logger.warning(f"Incomplete indicators: " f"{symbol}")

                    continue

                # ======================================
                # SAVE CACHE
                # ======================================

                df.to_parquet(cache_path, index=True)

                logger.info(f"Saved cache: {symbol}")

                return True

            except Exception as retry_error:

                logger.warning(
                    f"Retry "
                    f"{attempt+1}/"
                    f"{max_retries} "
                    f"{symbol}: "
                    f"{retry_error}"
                )

                time.sleep(2)

        logger.error(f"Download failed: {symbol}")

        return False

    except Exception as e:

        logger.error(f"Download Error " f"{symbol}: {e}")

        return False


# ======================================
# MAIN ENGINE
# ======================================


def main():

    try:

        logger.info("DOWNLOAD MARKET DATA STARTED")

        audit_event("DOWNLOAD_START", "Market download pipeline")

        success = 0

        failed = 0

        total = len(IDX_STOCKS)

        # ======================================
        # PARALLEL DOWNLOAD
        # ======================================

        with ThreadPoolExecutor(max_workers=4) as executor:

            results = list(
                executor.map(safe_execute, [download_stock] * total, IDX_STOCKS)
            )

        # ======================================
        # SUMMARY
        # ======================================

        for result in results:

            if result:

                success += 1

            else:

                failed += 1

        # ======================================
        # HEALTH SCORE
        # ======================================

        success_rate = round((success / total) * 100, 2)

        health_status = "HEALTHY"

        if success_rate < 90:

            health_status = "WARNING"

        if success_rate < 70:

            health_status = "CRITICAL"

        # ======================================
        # FINAL LOG
        # ======================================

        logger.info("=================================")

        logger.info("DOWNLOAD COMPLETE")

        logger.info(f"Success: {success}")

        logger.info(f"Failed: {failed}")

        logger.info(f"Success Rate: " f"{success_rate}%")

        logger.info(f"Health: " f"{health_status}")

        logger.info("=================================")

        audit_event("DOWNLOAD_COMPLETE", f"Success={success} " f"Failed={failed}")

    except Exception as e:

        logger.error(f"Pipeline Error: {e}")


# ======================================
# ENTRY POINT
# ======================================

if __name__ == "__main__":

    main()
