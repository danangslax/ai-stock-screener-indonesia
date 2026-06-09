import streamlit as st
import yfinance as yf
import pandas as pd

@st.cache_data(ttl=3600)
def load_stock_data(symbol):

    df = yf.download(
        symbol,
        period="3mo",
        interval="1d",
        auto_adjust=True,
        progress=False
    )

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    return df
