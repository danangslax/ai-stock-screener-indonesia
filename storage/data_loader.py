import yfinance as yf
import pandas as pd

from pathlib import Path

# ======================================
# CACHE DIRECTORY
# ======================================

CACHE_DIR = Path("data") / "cache"

CACHE_DIR.mkdir(parents=True, exist_ok=True)

# ======================================
# LOAD STOCK DATA
# ======================================


def load_stock_data(
    symbol, period="1y", interval="1d", use_cache=True, cache_only=False
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

                df = pd.read_parquet(cache_path)

                # ======================================
                # VALIDATION
                # ======================================

                if not df.empty:

                    print(f"⚡ Cache loaded " f"{symbol}")

                    return df

            except Exception as e:

                print(f"⚠️ Cache read error " f"{symbol}: {e}")

            # ======================================
            # CACHE ONLY MODE
            # ======================================

            if cache_only:

                print(f"⚠️ Cache only mode " f"{symbol}")

                return pd.DataFrame()

        # ======================================
        # FALLBACK YFINANCE
        # ======================================

        print(f"⬇️ Downloading " f"{symbol}")

        df = yf.download(
            symbol, period=period, interval=interval, auto_adjust=True, progress=False
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

            print(f"⚠️ Empty data " f"{symbol}")

            return pd.DataFrame()

        # ======================================
        # SAVE CACHE
        # ======================================

        try:

            df.to_parquet(cache_path)

        except Exception as e:

            print(f"⚠️ Cache save error " f"{symbol}: {e}")

        print(f"✅ Data loaded " f"{symbol}")

        return df

    except Exception as e:

        print(f"❌ Data Loader Error " f"{symbol}: {e}")

        return pd.DataFrame()
