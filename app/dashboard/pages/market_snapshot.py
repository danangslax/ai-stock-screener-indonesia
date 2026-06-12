import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from pathlib import Path

from market.market_snapshot import build_market_snapshot
from market.market_intelligence import generate_market_intelligence
from market.market import get_market_status
from market.market_breadth import analyze_market_breadth
from market.sector_strength import analyze_sector_strength

# ======================================
# WATCHLIST
# ======================================

WATCHLIST_PATH = Path("watchlist") / "idx_stocks.txt"

# ======================================
# LOAD WATCHLIST
# ======================================

IDX_STOCKS = []

if WATCHLIST_PATH.exists():

    with open(WATCHLIST_PATH, "r", encoding="utf-8") as f:

        IDX_STOCKS = [line.strip() for line in f if line.strip()]

# ======================================
# MARKET SNAPSHOT PAGE
# ======================================


def render_market_snapshot():

    st.header("🌍 Market Snapshot")

    # ======================================
    # BUILD SNAPSHOT
    # ======================================

    with st.spinner("Analyzing market..."):

        snapshot = build_market_snapshot(IDX_STOCKS)

    # ======================================
    # VALIDATION
    # ======================================

    if not snapshot:

        st.error("Failed to build market snapshot")

        return

    # ======================================
    # MARKET METRICS
    # ======================================

    st.subheader("📊 Market Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Market Status",
            snapshot.get("market_status", "UNKNOWN"),
        )

    with col2:

        st.metric(
            "Breadth Score",
            snapshot.get("breadth_score", 0),
        )

    with col3:

        st.metric(
            "Strongest Sector",
            snapshot.get("strongest_sector", "N/A"),
        )

    with col4:

        st.metric(
            "Market Bias",
            snapshot.get("market_bias", "DEFENSIVE"),
        )

    # ======================================
    # MARKET DETAIL
    # ======================================

    st.subheader("📈 Market Detail")

    market_detail = get_market_status()

    detail1, detail2, detail3, detail4 = st.columns(4)

    with detail1:

        st.metric(
            "IHSG Change %",
            market_detail.get("change", 0),
        )

    with detail2:

        st.metric(
            "RSI",
            market_detail.get("rsi", 0),
        )

    with detail3:

        st.metric(
            "ADX",
            market_detail.get("adx", 0),
        )

    with detail4:

        st.metric(
            "Volatility",
            market_detail.get("volatility", 0),
        )

    # ======================================
    # MARKET BREADTH
    # ======================================

    st.subheader("🔥 Market Breadth")

    breadth = analyze_market_breadth(IDX_STOCKS)

    if breadth:

        b1, b2 = st.columns(2)

        with b1:

            st.info(f"""
Above MA20:
{breadth['above_ma20_pct']}%
""")

            st.info(f"""
Bullish RSI:
{breadth['bullish_rsi_pct']}%
""")

        with b2:

            st.info(f"""
Breakout Stocks:
{breadth['breakout_pct']}%
""")

            st.info(f"""
Strong Relative Strength:
{breadth['strong_rs_pct']}%
""")

        # ======================================
        # BREADTH CHART
        # ======================================

        breadth_fig = go.Figure()

        categories = [
            "Above MA20",
            "Bullish RSI",
            "Breakout",
            "Strong RS",
        ]

        values = [
            breadth["above_ma20_pct"],
            breadth["bullish_rsi_pct"],
            breadth["breakout_pct"],
            breadth["strong_rs_pct"],
        ]

        breadth_fig.add_trace(
            go.Bar(
                x=categories,
                y=values,
                text=values,
                textposition="auto",
            )
        )

        breadth_fig.update_layout(
            height=400,
            template="plotly_dark",
            title="Market Breadth Analysis",
        )

        st.plotly_chart(
            breadth_fig,
            use_container_width=True,
        )

    else:

        st.warning("Breadth analysis unavailable")

    # ======================================
    # SECTOR STRENGTH
    # ======================================

    st.subheader("🏭 Sector Strength")

    sector_df = analyze_sector_strength()

    if not sector_df.empty:

        # ======================================
        # TOP SECTOR
        # ======================================

        top_sector = sector_df.iloc[0]

        top1, top2, top3 = st.columns(3)

        with top1:

            st.metric(
                "Top Sector",
                top_sector["Sector"],
            )

        with top2:

            st.metric(
                "Sector Score",
                top_sector["Score"],
            )

        with top3:

            st.metric(
                "Sector Leader",
                top_sector["Leader"],
            )

        # ======================================
        # SECTOR CHART
        # ======================================

        sector_fig = go.Figure()

        sector_fig.add_trace(
            go.Bar(
                x=sector_df["Sector"],
                y=sector_df["Score"],
                text=sector_df["Score"],
                textposition="auto",
            )
        )

        sector_fig.update_layout(
            height=500,
            template="plotly_dark",
            title="Sector Strength Ranking",
        )

        st.plotly_chart(
            sector_fig,
            use_container_width=True,
        )

        # ======================================
        # SECTOR TABLE
        # ======================================

        st.subheader("📋 Sector Ranking")

        display_columns = [
            "Sector",
            "Score",
            "Average_Return",
            "Average_RSI",
            "Average_RS",
            "Bullish_%",
            "Leader",
            "Status",
        ]

        sector_display = sector_df[display_columns].copy()

        sector_display = sector_display.round(2)

        st.dataframe(
            sector_display,
            use_container_width=True,
        )

    else:

        st.warning("Sector analysis unavailable")

    # ======================================
    # AI MARKET INTELLIGENCE
    # ======================================

    st.subheader("🧠 AI Market Intelligence")

    intelligence = generate_market_intelligence(snapshot)

    st.text_area(
        "Market Commentary",
        intelligence,
        height=350,
    )

    # ======================================
    # MARKET INTERPRETATION
    # ======================================

    st.subheader("🎯 Market Interpretation")

    market_status = snapshot.get("market_status", "UNKNOWN")

    interpretation = ""

    if market_status == "STRONG_BULL":

        interpretation = """
🔥 Strong bullish market.

Best Strategy:
- Breakout trading
- Momentum continuation
- Aggressive swing trading
"""

    elif market_status == "BULL":

        interpretation = """
📈 Bullish market condition.

Best Strategy:
- Buy pullback
- Trend following
- Sector rotation
"""

    elif market_status == "ACCUMULATION":

        interpretation = """
🏗️ Accumulation phase.

Best Strategy:
- Support buying
- Early positioning
- Focus on leader stocks
"""

    elif market_status == "SIDEWAYS":

        interpretation = """
↔️ Sideways market.

Best Strategy:
- Quick swing
- Range trading
- Tight risk management
"""

    elif market_status == "BEARISH":

        interpretation = """
🐻 Bearish market.

Best Strategy:
- Defensive trading
- Reduce exposure
- Preserve capital
"""

    elif market_status == "PANIC":

        interpretation = """
🚨 Panic market condition.

Best Strategy:
- Cash preservation
- Avoid aggressive trading
- Wait for stabilization
"""

    elif market_status == "RECOVERY":

        interpretation = """
🌱 Recovery phase.

Best Strategy:
- Early trend capture
- Watch new leaders
- Selective accumulation
"""

    else:

        interpretation = """
⚠️ Market status unclear.

Best Strategy:
- Stay selective
- Focus on risk management
"""

    st.info(interpretation)

    # ======================================
    # SNAPSHOT JSON
    # ======================================

    with st.expander("📦 Raw Snapshot Data"):

        st.json(snapshot)
