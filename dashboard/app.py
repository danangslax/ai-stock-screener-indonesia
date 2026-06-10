import sys
from pathlib import Path

# ======================================
# ROOT PATH FIX
# ======================================

sys.path.append(
    str(
        Path(__file__)
        .resolve()
        .parent
        .parent
    )
)

# ======================================
# IMPORTS
# ======================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from core.indicators import (
    add_indicators
)

from core.data_loader import (
    load_stock_data
)

from core.market import (
    get_market_status
)

from core.trade_plan import (
    generate_trade_plan
)

from database.queries import (
    load_screener_history
)

from core.paper_trading import (
    create_trade,
    load_trades
)

from core.analytics import (

    calculate_portfolio_metrics,
    generate_equity_curve
)

from core.backtest import (
    run_backtest
)

from core.sector_strength import (
    analyze_sector_strength
)


# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(

    page_title=(
        "AI Stock Screener Indonesia"
    ),

    layout="wide"
)

# ======================================
# BASE DIRECTORY
# ======================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

# ======================================
# WATCHLIST PATH
# ======================================

WATCHLIST_PATH = (
    BASE_DIR
    / "watchlist"
    / "idx_stocks.txt"
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

st.sidebar.title(
    "📌 Watchlist"
)

try:

    with open(

        WATCHLIST_PATH,

        "r",

        encoding="utf-8"
    ) as f:

        watchlist = [

            line
            .strip()
            .replace(".JK", "")

            for line in f

            if line.strip()
        ]

except Exception as e:

    st.error(
        f"Watchlist error: {e}"
    )

    st.stop()

# ======================================
# SELECT WATCHLIST
# ======================================

selected_watchlist = (
    st.sidebar.selectbox(

        "Pilih saham",

        watchlist
    )
)

# ======================================
# INPUT
# ======================================

ticker = st.text_input(

    "Masukkan kode saham IDX",

    value=selected_watchlist
)

symbol = (
    f"{ticker.upper()}.JK"
)

# ======================================
# LOAD DATA
# ======================================

try:

    df = load_stock_data(symbol)

except Exception as e:

    st.error(
        f"Data loading error: {e}"
    )

    st.stop()

# ======================================
# VALIDATION
# ======================================

if df.empty:

    st.error(
        "Data saham tidak ditemukan"
    )

    st.stop()

# ======================================
# ADD INDICATORS
# ======================================

try:

    df = add_indicators(df)

except Exception as e:

    st.error(
        f"Indicator error: {e}"
    )

    st.stop()

# ======================================
# DATA VALIDATION
# ======================================

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

close_price = float(
    latest["Close"]
)

volume = float(
    latest["Volume"]
)

change_percent = (

    (
        close_price
        -
        previous["Close"]
    )

    /

    previous["Close"]

) * 100

# ======================================
# STOCK OVERVIEW
# ======================================

st.subheader(
    "📌 Stock Overview"
)

col1, col2, col3 = (
    st.columns(3)
)

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

col1, col2, col3, col4 = (
    st.columns(4)
)

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

# ======================================
# CANDLESTICK
# ======================================

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

# ======================================
# BOLLINGER BANDS
# ======================================

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

# ======================================
# LAYOUT
# ======================================

fig.update_layout(

    height=600,

    xaxis_rangeslider_visible=False
)

# ======================================
# SHOW CHART
# ======================================

st.plotly_chart(

    fig,

    use_container_width=True
)

# ======================================
# HISTORICAL DATA
# ======================================

st.subheader(
    "📜 Historical Data"
)

st.dataframe(

    df.tail(20),

    use_container_width=True
)

# ======================================
# REFRESH BUTTON
# ======================================

st.divider()

if st.button(
    "🔄 Refresh Data"
):

    st.cache_data.clear()

    st.rerun()

# ======================================
# MARKET STATUS
# ======================================

st.header(
    "📊 Market Status"
)

try:

    market = get_market_status()

    if (
        market["status"]
        == "BULLISH"
    ):

        st.success(

            f"IHSG Bullish "
            f"({market['change']}%)"
        )

    elif (
        market["status"]
        == "BEARISH"
    ):

        st.error(

            f"IHSG Bearish "
            f"({market['change']}%)"
        )

    else:

        st.warning(

            f"IHSG Sideways "
            f"({market['change']}%)"
        )

except Exception as e:

    st.error(
        f"Market status error: {e}"
    )

# ======================================
# LATEST AI SCREENER
# ======================================

st.divider()

st.header(
    "🔥 Latest AI Screener"
)

# ======================================
# LOAD SCREENER HISTORY
# ======================================

try:

    history = (
        load_screener_history()
    )

except Exception as e:

    st.error(
        f"Database error: {e}"
    )

    history = []

# ======================================
# DISPLAY RESULTS
# ======================================

if history:

    screener_df = pd.DataFrame(
        history
    )

    # ======================================
    # TOP PICK
    # ======================================

    top_pick = (
        screener_df.iloc[0]
    )

    st.subheader(
        "🏆 Top Pick"
    )

    col1, col2, col3 = (
        st.columns(3)
    )

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

    trade_plan = (
        generate_trade_plan(
            top_pick["Price"]
        )
    )

    st.subheader(
        "📌 Trade Plan"
    )

    col1, col2, col3, col4 = (
        st.columns(4)
    )

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

        trade_plan[
            "risk_reward"
        ]
    )

    # ======================================
    # PAPER TRADING
    # ======================================

    st.subheader(
        "💰 Paper Trading"
    )

    if st.button(
        "📈 Buy Top Pick"
    ):

        try:

            create_trade(

                symbol=(
                    top_pick["Symbol"]
                ),

                buy_price=float(
                    top_pick["Price"]
                ),

                quantity=1
            )

            st.success(
                "Paper trade berhasil dibuat"
            )

        except Exception as e:

            st.error(
                f"Trade error: {e}"
            )

    # ======================================
    # RESULT TABLE
    # ======================================

    st.subheader(
        "📊 Latest Screening Results"
    )

    st.dataframe(

        screener_df,

        use_container_width=True
    )

else:

    st.info(
        "Belum ada hasil screening"
    )

# ======================================
# PORTFOLIO ANALYTICS
# ======================================

st.divider()

st.header(
    "📊 Portfolio Analytics"
)

try:

    analytics_trades = (
        load_trades()
    )

except Exception as e:

    st.error(
        f"Analytics error: {e}"
    )

    analytics_trades = []

# ======================================
# CALCULATE METRICS
# ======================================

metrics = calculate_portfolio_metrics(
    analytics_trades
)

# ======================================
# METRICS ROW 1
# ======================================

col1, col2, col3, col4 = (
    st.columns(4)
)

col1.metric(

    "Total Trades",

    metrics["total_trades"]
)

col2.metric(

    "Winrate",

    f"{metrics['winrate']}%"
)

col3.metric(

    "Total PnL",

    f"Rp {metrics['total_pnl']:,.0f}"
)

col4.metric(

    "Profit Factor",

    metrics["profit_factor"]
)

# ======================================
# METRICS ROW 2
# ======================================

col1, col2, col3, col4 = (
    st.columns(4)
)

col1.metric(

    "Winning Trades",

    metrics["winning_trades"]
)

col2.metric(

    "Losing Trades",

    metrics["losing_trades"]
)

col3.metric(

    "Average RR",

    metrics["average_rr"]
)

col4.metric(

    "Expectancy",

    metrics["expectancy"]
)

# ======================================
# BEST / WORST
# ======================================

col1, col2 = st.columns(2)

col1.success(

    f"🏆 Best Trade: "
    f"Rp {metrics['best_trade']:,.0f}"
)

col2.error(

    f"📉 Worst Trade: "
    f"Rp {metrics['worst_trade']:,.0f}"
)

# ======================================
# EQUITY CURVE
# ======================================

equity_df = generate_equity_curve(
    analytics_trades
)

if not equity_df.empty:

    st.subheader(
        "📈 Equity Curve"
    )

    equity_fig = go.Figure()

    equity_fig.add_trace(

        go.Scatter(

            x=equity_df.index,

            y=equity_df["equity"],

            mode="lines",

            name="Equity"
        )
    )

    equity_fig.update_layout(

        height=400,

        xaxis_title="Trade",

        yaxis_title="Balance"
    )

    st.plotly_chart(

        equity_fig,

        use_container_width=True
    )

# ======================================
# SECTOR STRENGTH
# ======================================

st.divider()

st.header(
    "🏭 Sector Strength Ranking"
)

# ======================================
# LOAD SECTOR DATA
# ======================================

with st.spinner(
    "Analyzing sectors..."
):

    sector_df = (
        analyze_sector_strength()
    )

# ======================================
# VALIDATION
# ======================================

if not sector_df.empty:

    # ======================================
    # TOP SECTOR
    # ======================================

    top_sector = sector_df.iloc[0]

    st.subheader(
        "🔥 Strongest Sector"
    )

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    col1.metric(

        "Sector",

        top_sector["Sector"]
    )

    col2.metric(

        "Score",

        top_sector["Score"]
    )

    col3.metric(

        "Leader",

        top_sector["Leader"]
    )

    col4.metric(

        "Bullish %",

        f"{top_sector['Bullish_%']}%"
    )

    # ======================================
    # SECTOR TABLE
    # ======================================

    st.subheader(
        "📊 Sector Ranking"
    )

    st.dataframe(

        sector_df,

        use_container_width=True
    )

    # ======================================
    # CHART
    # ======================================

    st.subheader(
        "📈 Sector Strength Chart"
    )

    sector_fig = go.Figure()

    sector_fig.add_trace(

        go.Bar(

            x=sector_df["Sector"],

            y=sector_df["Score"],

            name="Sector Score"
        )
    )

    sector_fig.update_layout(

        height=500,

        xaxis_title="Sector",

        yaxis_title="Score"
    )

    st.plotly_chart(

        sector_fig,

        use_container_width=True
    )

else:

    st.warning(
        "Sector data not available"
    )

# ======================================
# BACKTEST DASHBOARD
# ======================================

st.divider()

st.header(
    "🧪 Strategy Backtest"
)

# ======================================
# BACKTEST INPUT
# ======================================

col1, col2 = st.columns(2)

backtest_symbol = col1.text_input(

    "Backtest Symbol",

    value=symbol
)

backtest_period = col2.selectbox(

    "Backtest Period",

    [

        "6mo",

        "1y",

        "2y",

        "5y"
    ]
)

# ======================================
# RUN BACKTEST
# ======================================

if st.button(
    "🚀 Run Backtest"
):

    with st.spinner(
        "Running backtest..."
    ):

        stats = run_backtest(

            backtest_symbol,

            period=backtest_period
        )

    # ======================================
    # VALIDATION
    # ======================================

    if stats is None:

        st.error(
            "Backtest gagal"
        )

    else:

        st.success(
            "Backtest selesai"
        )

        # ======================================
        # METRICS
        # ======================================

        col1, col2, col3, col4 = (
            st.columns(4)
        )

        col1.metric(

            "Return %",

            round(
                stats["Return [%]"],
                2
            )
        )

        col2.metric(

            "Win Rate %",

            round(
                stats["Win Rate [%]"],
                2
            )
        )

        col3.metric(

            "Max Drawdown %",

            round(
                stats["Max. Drawdown [%]"],
                2
            )
        )

        col4.metric(

            "Total Trades",

            int(
                stats["# Trades"]
            )
        )

        # ======================================
        # SECOND ROW
        # ======================================

        col1, col2, col3, col4 = (
            st.columns(4)
        )

        col1.metric(

            "Sharpe Ratio",

            round(
                stats["Sharpe Ratio"],
                2
            )
        )

        col2.metric(

            "Profit Factor",

            round(
                stats["Profit Factor"],
                2
            )
        )

        col3.metric(

            "Expectancy",

            round(
                stats["Expectancy [%]"],
                2
            )
        )

        col4.metric(

            "SQN",

            round(
                stats["SQN"],
                2
            )
        )

        # ======================================
        # EQUITY CURVE
        # ======================================

        st.subheader(
            "📈 Backtest Equity Curve"
        )

        equity_curve = (
            stats["_equity_curve"]
        )

        equity_fig = go.Figure()

        equity_fig.add_trace(

            go.Scatter(

                x=equity_curve.index,

                y=equity_curve["Equity"],

                mode="lines",

                name="Equity"
            )
        )

        equity_fig.update_layout(

            height=400,

            xaxis_title="Date",

            yaxis_title="Equity"
        )

        st.plotly_chart(

            equity_fig,

            use_container_width=True
        )

        # ======================================
        # TRADES
        # ======================================

        st.subheader(
            "📋 Trade History"
        )

        trades_df = stats[
            "_trades"
        ]

        st.dataframe(

            trades_df,

            use_container_width=True
        )

# ======================================
# PAPER TRADING HISTORY
# ======================================

st.divider()

st.header(
    "📒 Paper Trading History"
)

try:

    trades = load_trades()

except Exception as e:

    st.error(
        f"Trade history error: {e}"
    )

    trades = []

# ======================================
# DISPLAY TRADES
# ======================================

if trades:

    trades_df = pd.DataFrame(
        trades
    )

    st.dataframe(

        trades_df,

        use_container_width=True
    )

else:

    st.info(
        "Belum ada paper trade"
    )