import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from screener.screener import run_screener
from market.market import get_market_status
from market.market_snapshot import build_market_snapshot
from ai.market_commentary import generate_market_commentary

# ======================================
# SCREENER DASHBOARD PAGE
# ======================================


def render_screener_dashboard():

    st.header("🤖 AI Screener Dashboard")

    # ======================================
    # CONTROL PANEL
    # ======================================

    st.subheader("⚙️ Screener Settings")

    col1, col2, col3 = st.columns(3)

    with col1:

        max_results = st.slider(
            "Maximum Results",
            min_value=5,
            max_value=50,
            value=15,
        )

    with col2:

        minimum_confidence = st.slider(
            "Minimum Confidence",
            min_value=50,
            max_value=100,
            value=70,
        )

    with col3:

        auto_refresh = st.checkbox(
            "Auto Refresh",
            value=False,
        )

    # ======================================
    # RUN SCREENER BUTTON
    # ======================================

    run_button = st.button(
        "🚀 Run AI Screener",
        use_container_width=True,
    )

    # ======================================
    # AUTO REFRESH
    # ======================================

    if auto_refresh:

        run_button = True

    # ======================================
    # RUN ENGINE
    # ======================================

    if run_button:

        with st.spinner("Running AI Screener..."):

            # ======================================
            # MARKET STATUS
            # ======================================

            market = get_market_status()

            # ======================================
            # SCREENER
            # ======================================

            screener_df, filtered_symbols = run_screener()

            # ======================================
            # SNAPSHOT
            # ======================================

            snapshot = build_market_snapshot(filtered_symbols)

            # ======================================
            # COMMENTARY
            # ======================================

            commentary = generate_market_commentary(
                snapshot,
                screener_df,
            )

        # ======================================
        # VALIDATION
        # ======================================

        if screener_df.empty:

            st.warning("No stocks passed the screening criteria")

            return

        # ======================================
        # FILTER CONFIDENCE
        # ======================================

        if "Confidence" in screener_df.columns:

            screener_df = screener_df[screener_df["Confidence"] >= minimum_confidence]

        # ======================================
        # LIMIT RESULTS
        # ======================================

        screener_df = screener_df.head(max_results)

        # ======================================
        # MARKET OVERVIEW
        # ======================================

        st.subheader("🌍 Market Overview")

        m1, m2, m3, m4 = st.columns(4)

        with m1:

            st.metric(
                "Market Status",
                market.get("status", "UNKNOWN"),
            )

        with m2:

            st.metric(
                "Market Bias",
                snapshot.get(
                    "market_bias",
                    "DEFENSIVE",
                ),
            )

        with m3:

            st.metric(
                "Breadth Score",
                snapshot.get(
                    "breadth_score",
                    0,
                ),
            )

        with m4:

            st.metric(
                "Total Picks",
                len(screener_df),
            )

        # ======================================
        # TOP PICK
        # ======================================

        st.subheader("🏆 Top AI Pick")

        top_pick = screener_df.iloc[0]

        tp1, tp2, tp3, tp4 = st.columns(4)

        with tp1:

            st.metric(
                "Symbol",
                top_pick["Symbol"],
            )

        with tp2:

            st.metric(
                "Price",
                round(
                    float(top_pick["Price"]),
                    2,
                ),
            )

        with tp3:

            st.metric(
                "Score",
                round(
                    float(top_pick["Score"]),
                    2,
                ),
            )

        with tp4:

            st.metric(
                "Confidence",
                round(
                    float(top_pick["Confidence"]),
                    2,
                ),
            )

        # ======================================
        # AI COMMENTARY
        # ======================================

        st.subheader("🧠 AI Market Commentary")

        st.text_area(
            "AI Commentary",
            commentary,
            height=250,
        )

        # ======================================
        # SCORE DISTRIBUTION
        # ======================================

        st.subheader("📈 Score Distribution")

        if "Score" in screener_df.columns:

            score_fig = go.Figure()

            score_fig.add_trace(
                go.Bar(
                    x=screener_df["Symbol"],
                    y=screener_df["Score"],
                    text=screener_df["Score"],
                    textposition="auto",
                )
            )

            score_fig.update_layout(
                height=450,
                template="plotly_dark",
                title="AI Score Ranking",
            )

            st.plotly_chart(
                score_fig,
                use_container_width=True,
            )

        # ======================================
        # CONFIDENCE DISTRIBUTION
        # ======================================

        st.subheader("🔥 Confidence Analysis")

        if "Confidence" in screener_df.columns:

            confidence_fig = go.Figure()

            confidence_fig.add_trace(
                go.Scatter(
                    x=screener_df["Symbol"],
                    y=screener_df["Confidence"],
                    mode="lines+markers",
                    name="Confidence",
                )
            )

            confidence_fig.update_layout(
                height=400,
                template="plotly_dark",
                title="Signal Confidence",
            )

            st.plotly_chart(
                confidence_fig,
                use_container_width=True,
            )

        # ======================================
        # STRATEGY BREAKDOWN
        # ======================================

        st.subheader("🎯 Strategy Breakdown")

        if "Strategy" in screener_df.columns:

            strategy_counts = screener_df["Strategy"].value_counts()

            strategy_fig = go.Figure()

            strategy_fig.add_trace(
                go.Pie(
                    labels=strategy_counts.index,
                    values=strategy_counts.values,
                    hole=0.4,
                )
            )

            strategy_fig.update_layout(
                height=450,
                template="plotly_dark",
                title="Strategy Distribution",
            )

            st.plotly_chart(
                strategy_fig,
                use_container_width=True,
            )

        # ======================================
        # TOP PICKS TABLE
        # ======================================

        st.subheader("📋 Top AI Picks")

        display_columns = []

        preferred_columns = [
            "Symbol",
            "Price",
            "Score",
            "Confidence",
            "Strategy",
            "Market",
            "RSI",
            "ADX",
            "Risk_Reward",
            "Stop_Loss",
            "Take_Profit",
        ]

        for col in preferred_columns:

            if col in screener_df.columns:

                display_columns.append(col)

        display_df = screener_df[display_columns].copy()

        numeric_columns = display_df.select_dtypes(include=["float", "int"]).columns

        display_df[numeric_columns] = display_df[numeric_columns].round(2)

        st.dataframe(
            display_df,
            use_container_width=True,
        )

        # ======================================
        # DOWNLOAD CSV
        # ======================================

        st.subheader("💾 Export Screener")

        csv = display_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="ai_screener_results.csv",
            mime="text/csv",
        )

        # ======================================
        # AI INSIGHT
        # ======================================

        st.subheader("🧠 AI Insight")

        average_score = round(
            screener_df["Score"].mean(),
            2,
        )

        average_confidence = round(
            screener_df["Confidence"].mean(),
            2,
        )

        insight = f"""
Total AI Picks:
{len(screener_df)}

Average Score:
{average_score}

Average Confidence:
{average_confidence}

Market Regime:
{market.get('status')}

Market Bias:
{snapshot.get('market_bias')}

Strongest Sector:
{snapshot.get('strongest_sector')}

Top Leader:
{snapshot.get('sector_leader')}
"""

        st.info(insight)

        # ======================================
        # RAW DATA
        # ======================================

        with st.expander("📦 Raw Screener Data"):

            st.dataframe(
                screener_df,
                use_container_width=True,
            )
