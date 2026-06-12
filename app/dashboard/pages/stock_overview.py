import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from storage.data_loader import load_stock_data
from storage.indicators import add_indicators

# ======================================
# STOCK OVERVIEW PAGE
# ======================================


def render_stock_overview():

    st.header("📊 Stock Overview")

    # ======================================
    # INPUTS
    # ======================================

    col1, col2, col3 = st.columns(3)

    with col1:

        symbol = st.text_input("Stock Symbol", value="BBRI.JK")

    with col2:

        period = st.selectbox(
            "Period",
            [
                "3mo",
                "6mo",
                "1y",
                "2y",
                "5y",
            ],
            index=2,
        )

    with col3:

        interval = st.selectbox(
            "Interval",
            [
                "1d",
                "1wk",
                "1mo",
            ],
            index=0,
        )

    # ======================================
    # LOAD DATA
    # ======================================

    with st.spinner("Loading stock data..."):

        df = load_stock_data(
            symbol=symbol,
            period=period,
            interval=interval,
        )

    # ======================================
    # VALIDATION
    # ======================================

    if df.empty:

        st.error("No stock data available")

        return

    # ======================================
    # ADD INDICATORS
    # ======================================

    df = add_indicators(df)

    if df.empty:

        st.error("Indicator processing failed")

        return

    # ======================================
    # LATEST DATA
    # ======================================

    latest = df.iloc[-1]

    # ======================================
    # METRICS
    # ======================================

    st.subheader("📌 Market Metrics")

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "Close",
            round(float(latest["Close"]), 2),
        )

    with m2:

        st.metric(
            "RSI",
            round(float(latest["RSI"]), 2),
        )

    with m3:

        st.metric(
            "ADX",
            round(float(latest["ADX"]), 2),
        )

    with m4:

        st.metric(
            "Volume",
            f"{int(latest['Volume']):,}",
        )

    # ======================================
    # TECHNICAL STATUS
    # ======================================

    st.subheader("🧠 Technical Analysis")

    close_price = float(latest["Close"])

    ema20 = float(latest["EMA20"])

    ema50 = float(latest["EMA50"])

    rsi = float(latest["RSI"])

    adx = float(latest["ADX"])

    trend = "NEUTRAL"

    if close_price > ema20 and ema20 > ema50:

        trend = "BULLISH"

    elif close_price < ema20 and ema20 < ema50:

        trend = "BEARISH"

    momentum = "WEAK"

    if rsi >= 60:

        momentum = "STRONG"

    elif rsi >= 50:

        momentum = "HEALTHY"

    strength = "LOW"

    if adx >= 25:

        strength = "STRONG"

    elif adx >= 20:

        strength = "MODERATE"

    t1, t2, t3 = st.columns(3)

    with t1:

        st.info(f"📈 Trend: {trend}")

    with t2:

        st.info(f"⚡ Momentum: {momentum}")

    with t3:

        st.info(f"🔥 Trend Strength: {strength}")

    # ======================================
    # CANDLESTICK CHART
    # ======================================

    st.subheader("📈 Price Chart")

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
            name="Price",
        )
    )

    # ======================================
    # MOVING AVERAGES
    # ======================================

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["EMA20"],
            mode="lines",
            name="EMA20",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["EMA50"],
            mode="lines",
            name="EMA50",
        )
    )

    # ======================================
    # LAYOUT
    # ======================================

    fig.update_layout(
        height=650,
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # ======================================
    # RSI CHART
    # ======================================

    st.subheader("⚡ RSI Analysis")

    rsi_fig = go.Figure()

    rsi_fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["RSI"],
            mode="lines",
            name="RSI",
        )
    )

    rsi_fig.add_hline(y=70)

    rsi_fig.add_hline(y=30)

    rsi_fig.update_layout(
        height=300,
        template="plotly_dark",
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),
    )

    st.plotly_chart(
        rsi_fig,
        use_container_width=True,
    )

    # ======================================
    # VOLUME CHART
    # ======================================

    st.subheader("📦 Volume Analysis")

    volume_fig = go.Figure()

    volume_fig.add_trace(
        go.Bar(
            x=df.index,
            y=df["Volume"],
            name="Volume",
        )
    )

    volume_fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["VOL_MA20"],
            mode="lines",
            name="VOL_MA20",
        )
    )

    volume_fig.update_layout(
        height=300,
        template="plotly_dark",
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),
    )

    st.plotly_chart(
        volume_fig,
        use_container_width=True,
    )

    # ======================================
    # HISTORICAL DATA
    # ======================================

    st.subheader("📋 Historical Data")

    display_columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "RSI",
        "ADX",
        "EMA20",
        "EMA50",
    ]

    historical_df = df[display_columns].copy()

    historical_df = historical_df.round(2)

    st.dataframe(
        historical_df.tail(100),
        use_container_width=True,
    )

    # ======================================
    # SUMMARY
    # ======================================

    st.subheader("📝 AI Summary")

    summary = f"""
    Symbol:
    {symbol}

    Current Trend:
    {trend}

    Momentum:
    {momentum}

    Trend Strength:
    {strength}

    RSI:
    {round(rsi, 2)}

    ADX:
    {round(adx, 2)}

    EMA20:
    {round(ema20, 2)}

    EMA50:
    {round(ema50, 2)}
    """

    st.text(summary)
