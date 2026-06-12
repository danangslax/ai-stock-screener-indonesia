import time

import yfinance as yf

import pandas as pd

from pathlib import Path

from infrastructure.logger import logger

from infrastructure.cache_validator import validate_cache_file

# ======================================
# CACHE DIRECTORY
# ======================================

CACHE_DIR = Path("data") / "cache"

CACHE_DIR.mkdir(parents=True, exist_ok=True)

# ======================================
# LOAD STOCK DATA
# ======================================


def load_stock_data(
    symbol, period="1y", interval="1d", use_cache=True, cache_only=False, retries=3
):

    try:

        # ======================================
        # CACHE PATH
        # ======================================

        cache_path = CACHE_DIR / f"{symbol}.parquet"

        # ======================================
        # LOAD CACHE
        # ======================================

        if use_cache and cache_path.exists():

            try:

                # ======================================
                # VALIDATE CACHE
                # ======================================

                if validate_cache_file(cache_path):

                    df = pd.read_parquet(cache_path)

                    logger.info(f"Cache loaded " f"{symbol}")

                    return df

                logger.warning(f"Invalid cache " f"{symbol}")

            except Exception as e:

                logger.warning(f"Cache read error " f"{symbol}: {e}")

        # ======================================
        # CACHE ONLY MODE
        # ======================================

        if cache_only:

            logger.warning(f"Cache only mode " f"{symbol}")

            return pd.DataFrame()

        # ======================================
        # DOWNLOAD RETRY LOOP
        # ======================================

        for attempt in range(retries):

            try:

                logger.info(f"Downloading " f"{symbol} " f"(Attempt " f"{attempt+1})")

                df = yf.download(
                    symbol,
                    period=period,
                    interval=interval,
                    auto_adjust=True,
                    progress=False,
                )

                # ======================================
                # FIX MULTI INDEX
                # ======================================

                if isinstance(df.columns, pd.MultiIndex):

                    df.columns = df.columns.get_level_values(0)

                # ======================================
                # REMOVE DUPLICATES
                # ======================================

                df = df[~df.index.duplicated(keep="last")]

                # ======================================
                # VALIDATION
                # ======================================

                if df.empty:

                    logger.warning(f"Empty data " f"{symbol}")

                    continue

                # ======================================
                # SORT INDEX
                # ======================================

                df = df.sort_index()

                # ======================================
                # SAVE CACHE
                # ======================================

                try:

                    df.to_parquet(cache_path)

                except Exception as e:

                    logger.warning(f"Cache save " f"error {symbol}: {e}")

                logger.info(f"Data loaded " f"{symbol}")

                return df

            except Exception as e:

                logger.warning(f"Download failed " f"{symbol}: {e}")

                time.sleep(2)

        # ======================================
        # FAILED AFTER RETRIES
        # ======================================

        logger.error(f"Failed to load " f"{symbol}")

        return pd.DataFrame()

    except Exception as e:

        logger.error(f"Data Loader Error " f"{symbol}: {e}")

        return pd.DataFrame()
