import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from core.indicators import add_indicators
from core.data_loader import load_stock_data
from core.market import get_market_status
from core.trade_plan import generate_trade_plan

from database.queries import (
    load_screener_history
)

from core.paper_trading import (
    create_trade,
    load_trades
)

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="AI Stock Screener Indonesia",
    layout="wide"
)

# ======================================
# TITLE
# ======================================

st.title(
    "📈 AI Stock Screener Indonesia"
)

# ======================================
# WATCHLIST
# ======================================

st.sidebar.title("📌 Watchlist")

with open("watchlist/idx_stocks.txt") as f:

    watchlist = [
        line.strip().replace(".JK", "")
        for line in f
        if line.strip()
    ]

selected_watchlist = st.sidebar.selectbox(
    "Pilih saham",
    watchlist
)

# ======================================
# INPUT
# ======================================

ticker = st.text_input(
    "Masukkan kode saham IDX",
    value=selected_watchlist
)

symbol = f"{ticker.upper()}.JK"

# ======================================
# LOAD DATA
# ======================================

df = load_stock_data(symbol)

if df.empty:

    st.error(
        "Data saham tidak ditemukan"
    )

    st.stop()

# ======================================
# ADD INDICATORS
# ======================================

df = add_indicators(df)

if len(df) < 2:

    st.warning(
        "Data saham belum cukup"
    )

    st.stop()

# ======================================
# LATEST DATA
# ======================================

latest = df.iloc[-1]
previous = df.iloc[-2]

close_price = latest["Close"]

volume = latest["Volume"]

change_percent = (
    (close_price - previous["Close"])
    / previous["Close"]
) * 100

# ======================================
# STOCK OVERVIEW
# ======================================

st.subheader("📌 Stock Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Last Price",
    f"Rp {close_price:,.2f}"
)

col2.metric(
    "Volume",
    f"{int(volume):,}"
)

col3.metric(
    "Change %",
    f"{change_percent:.2f}%"
)

# ======================================
# TECHNICAL INDICATORS
# ======================================

st.subheader(
    "📊 Technical Indicators"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "MA5",
    f"{latest['MA5']:.2f}"
)

col2.metric(
    "MA20",
    f"{latest['MA20']:.2f}"
)

col3.metric(
    "RSI",
    f"{latest['RSI']:.2f}"
)

col4.metric(
    "VOL MA20",
    f"{int(latest['VOL_MA20']):,}"
)

# ======================================
# CHART
# ======================================

fig = go.Figure()

# Candlestick
fig.add_trace(
    go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Price"
    )
)

# Bollinger Bands
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["BB_UPPER"],
        name="BB Upper"
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["BB_MIDDLE"],
        name="BB Middle"
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["BB_LOWER"],
        name="BB Lower"
    )
)

fig.update_layout(
    height=600,
    xaxis_rangeslider_visible=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ======================================
# HISTORICAL DATA
# ======================================

st.subheader("📜 Historical Data")

st.dataframe(
    df.tail(20),
    use_container_width=True
)

# ======================================
# REFRESH BUTTON
# ======================================

st.divider()

if st.button("🔄 Refresh Data"):

    st.cache_data.clear()

    st.rerun()

# ======================================
# MARKET STATUS
# ======================================

st.header("📊 Market Status")

market = get_market_status()

if market["status"] == "BULLISH":

    st.success(
        f"IHSG Bullish ({market['change']}%)"
    )

elif market["status"] == "BEARISH":

    st.error(
        f"IHSG Bearish ({market['change']}%)"
    )

else:

    st.warning(
        f"IHSG Sideways ({market['change']}%)"
    )

# ======================================
# LATEST AI SCREENER
# ======================================

st.divider()

st.header("🔥 Latest AI Screener")

history = load_screener_history()

if history:

    screener_df = pd.DataFrame(history)

    # ======================================
    # TOP PICK
    # ======================================

    top_pick = screener_df.iloc[0]

    st.subheader("🏆 Top Pick")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Symbol",
        top_pick["Symbol"]
    )

    col2.metric(
        "Score",
        top_pick["Score"]
    )

    col3.metric(
        "RSI",
        top_pick["RSI"]
    )

    # ======================================
    # TRADE PLAN
    # ======================================

    trade_plan = generate_trade_plan(
        top_pick["Price"]
    )

    st.subheader("📌 Trade Plan")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Entry",
        trade_plan["entry"]
    )

    col2.metric(
        "Stop Loss",
        trade_plan["stop_loss"]
    )

    col3.metric(
        "Take Profit",
        trade_plan["take_profit"]
    )

    col4.metric(
        "Risk Reward",
        trade_plan["risk_reward"]
    )

    # ======================================
    # PAPER TRADING
    # ======================================

    st.subheader("💰 Paper Trading")

    if st.button("📈 Buy Top Pick"):

        create_trade(
            symbol=top_pick["Symbol"],
            buy_price=float(
                top_pick["Price"]
            ),
            quantity=1
        )

        st.success(
            "Paper trade berhasil dibuat"
        )

    # ======================================
    # RESULT TABLE
    # ======================================

    st.subheader("📊 Latest Screening Results")

    st.dataframe(
        screener_df,
        use_container_width=True
    )

else:

    st.info(
        "Belum ada hasil screening"
    )

# ======================================
# PAPER TRADES
# ======================================

st.divider()

st.header("📒 Paper Trading History")

trades = load_trades()

if trades:

    trades_df = pd.DataFrame(trades)

    st.dataframe(
        trades_df,
        use_container_width=True
    )

else:

    st.info(
        "Belum ada paper trade"
    )