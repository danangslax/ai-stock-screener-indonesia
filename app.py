import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from core.indicators import add_indicators
from core.screener import run_screener
from core.data_loader import load_stock_data
from core.notifier import send_telegram_message
from core.confirmation import morning_confirmation



from database.queries import (
    save_screener_results,
    load_screener_history
)

from core.paper_trading import (
    create_trade,
    close_trade,
    load_trades
)

from core.backtest import (
    run_backtest
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

st.title("📈 AI Stock Screener Indonesia")

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

st.sidebar.write(
    f"Selected: {selected_watchlist}"
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

    st.error("Data saham tidak ditemukan")

    st.stop()

# ======================================
# ADD INDICATORS
# ======================================

df = add_indicators(df)

if len(df) < 2:

    st.warning("Data saham belum cukup")

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

colA, colB, colC = st.columns(3)

colA.metric(
    "Last Price",
    f"Rp {close_price:,.2f}"
)

colB.metric(
    "Volume",
    f"{int(volume):,}"
)

colC.metric(
    "Change %",
    f"{change_percent:.2f}%"
)

# ======================================
# TECHNICAL INDICATORS
# ======================================

st.subheader("Technical Indicators")

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

# Bollinger Upper
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["BB_UPPER"],
        name="BB Upper"
    )
)

# Bollinger Middle
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["BB_MIDDLE"],
        name="BB Middle"
    )
)

# Bollinger Lower
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

st.subheader("Historical Data")

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

ihsg = load_stock_data("^JKSE")

if not ihsg.empty and len(ihsg) >= 2:

    ihsg_latest = ihsg.iloc[-1]
    ihsg_prev = ihsg.iloc[-2]

    ihsg_change = (
        (ihsg_latest["Close"] - ihsg_prev["Close"])
        / ihsg_prev["Close"]
    ) * 100

    if ihsg_change > 1:

        st.success(
            f"IHSG Bullish ({ihsg_change:.2f}%)"
        )

    elif ihsg_change < -1:

        st.error(
            f"IHSG Bearish ({ihsg_change:.2f}%)"
        )

    else:

        st.warning(
            f"IHSG Sideways ({ihsg_change:.2f}%)"
        )

# ======================================
# AI SCREENER
# ======================================

st.divider()

st.header("🔥 AI Stock Screener")

if st.button("Run Screener"):

    with st.spinner("Scanning saham IDX..."):

        screener_df = run_screener()

    # ======================================
    # EMPTY RESULT
    # ======================================

    if screener_df.empty:

        st.warning(
            "Tidak ada saham yang lolos filter"
        )

    else:

        st.success("Screening selesai")

        # ======================================
        # SAVE DATABASE
        # ======================================

        save_screener_results(
            screener_df
        )

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
        # MORNING CONFIRMATION
        # ======================================

        confirmation = morning_confirmation(
            top_pick["Symbol"]
        )

        st.subheader(
            "☀️ Morning Confirmation"
        )

        if confirmation == "BUY":

            st.success("BUY")

        elif confirmation == "WATCH":

            st.warning("WATCH")

        elif confirmation == "AVOID":

            st.error("AVOID")

        else:

            st.info(confirmation)

        # ======================================
        # TELEGRAM ALERT
        # ======================================

        message = f"""
🔥 TOP PICK TODAY

{top_pick["Symbol"]}

Score: {top_pick["Score"]}
RSI: {top_pick["RSI"]}

Morning Confirmation: {confirmation}

AI breakout detected
"""

        send_telegram_message(message)

        # ======================================
        # RESULT TABLE
        # ======================================

        st.dataframe(
            screener_df,
            use_container_width=True
        )

# ======================================
# SCREENING HISTORY
# ======================================

st.divider()

st.header("📜 Screening History")

history = load_screener_history()

if history:

    history_df = pd.DataFrame(history)

    st.dataframe(
        history_df,
        use_container_width=True
    )

else:

    st.info(
        "Belum ada history screening"
    )
    
# ======================================
# PAPER TRADING
# ======================================

st.divider()

st.header("💰 Paper Trading")

if "top_pick" in locals():

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
# LOAD TRADES
# ======================================

trades = load_trades()

if trades:

    trades_df = pd.DataFrame(trades)

    st.dataframe(
        trades_df,
        use_container_width=True
    )