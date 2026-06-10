import streamlit as st
import yfinance as yf
import pandas as pd

# ======================================
# LOAD STOCK DATA
# ======================================

@st.cache_data(ttl=3600)

def load_stock_data(

    symbol,

    period="6mo",

    interval="1d"
):

    try:

        print(
            f"📥 Loading data: {symbol}"
        )

        # ======================================
        # DOWNLOAD DATA
        # ======================================

        df = yf.download(

            symbol,

            period=period,

            interval=interval,

            auto_adjust=True,

            progress=False,

            threads=False
        )

        # ======================================
        # FIX MULTI INDEX
        # ======================================

        if isinstance(
            df.columns,
            pd.MultiIndex
        ):

            df.columns = (
                df.columns.get_level_values(0)
            )

        # ======================================
        # VALIDATION
        # ======================================

        if df.empty:

            print(
                f"⚠️ Empty data: {symbol}"
            )

            return pd.DataFrame()

        required_columns = [

            "Open",

            "High",

            "Low",

            "Close",

            "Volume"
        ]

        for column in required_columns:

            if column not in df.columns:

                print(
                    f"❌ Missing column: "
                    f"{column}"
                )

                return pd.DataFrame()

        # ======================================
        # CLEAN DATA
        # ======================================

        df = df.copy()

        df = df.dropna()

        df = df.sort_index()

        # ======================================
        # REMOVE DUPLICATES
        # ======================================

        df = df[
            ~df.index.duplicated(
                keep="last"
            )
        ]

        # ======================================
        # VALIDATION AFTER CLEANING
        # ======================================

        if len(df) < 20:

            print(
                f"⚠️ Not enough data: "
                f"{symbol}"
            )

            return pd.DataFrame()

        print(
            f"✅ Loaded: {symbol} "
            f"({len(df)} rows)"
        )

        return df

    except Exception as e:

        print(
            f"❌ Data Loader Error "
            f"{symbol}: {e}"
        )

        return pd.DataFrame()


# ======================================
# LOAD MULTIPLE STOCKS
# ======================================

def load_multiple_stocks(

    symbols,

    period="6mo",

    interval="1d"
):

    try:

        all_data = {}

        for symbol in symbols:

            df = load_stock_data(

                symbol,

                period=period,

                interval=interval
            )

            if not df.empty:

                all_data[symbol] = df

        print(
            f"✅ Loaded "
            f"{len(all_data)} stocks"
        )

        return all_data

    except Exception as e:

        print(
            f"❌ Multi Loader Error: {e}"
        )

        return {}


# ======================================
# CLEAR CACHE
# ======================================

def clear_data_cache():

    try:

        st.cache_data.clear()

        print(
            "🧹 Cache cleared"
        )

    except Exception as e:

        print(
            f"❌ Cache Clear Error: {e}"
        )