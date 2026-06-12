import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from trading.trade_journal import (
    load_journal,
)

from ai.learning_engine import (
    analyze_learning_data,
)

from ai.validation_engine import (
    validate_strategy_by_regime,
)

# ======================================
# AI LEARNING DASHBOARD PAGE
# ======================================


def render_ai_learning_dashboard():

    st.header("🧠 AI Learning Dashboard")

    # ======================================
    # LOAD JOURNAL
    # ======================================

    journal_data = load_journal()

    # ======================================
    # VALIDATION
    # ======================================

    if not journal_data:

        st.warning("No learning data available")

        return

    # ======================================
    # LEARNING ENGINE
    # ======================================

    learning_df = analyze_learning_data(journal_data)

    # ======================================
    # HEADER METRICS
    # ======================================

    st.subheader("📊 Learning Overview")

    total_entries = len(journal_data)

    high_confidence = len(
        [
            x
            for x in journal_data
            if x.get(
                "confidence",
                0,
            )
            >= 80
        ]
    )

    total_wins = len(
        [
            x
            for x in journal_data
            if "+"
            in str(
                x.get(
                    "result",
                    "",
                )
            )
        ]
    )

    winrate = 0

    if total_entries > 0:

        winrate = round(
            (total_wins / total_entries) * 100,
            2,
        )

    m1, m2, m3 = st.columns(3)

    with m1:

        st.metric(
            "Journal Entries",
            total_entries,
        )

    with m2:

        st.metric(
            "High Confidence",
            high_confidence,
        )

    with m3:

        st.metric(
            "Winrate",
            f"{winrate}%",
        )

    # ======================================
    # LEARNING TABLE
    # ======================================

    st.subheader("🤖 AI Learning Analysis")

    if not learning_df.empty:

        st.dataframe(
            learning_df,
            use_container_width=True,
        )

    else:

        st.warning("Learning analysis unavailable")

    # ======================================
    # WINRATE CHART
    # ======================================

    st.subheader("🏆 Strategy Winrate")

    if not learning_df.empty:

        chart_df = learning_df.copy()

        chart_df["Label"] = chart_df["Strategy"] + " | " + chart_df["Market_Regime"]

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=chart_df["Label"],
                y=chart_df["Winrate"],
                name="Winrate",
            )
        )

        fig.update_layout(
            height=500,
            template="plotly_dark",
            title="AI Strategy Learning",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # ======================================
    # CONFIDENCE ANALYSIS
    # ======================================

    st.subheader("⚡ Confidence Analysis")

    if not learning_df.empty:

        conf_fig = go.Figure()

        conf_fig.add_trace(
            go.Scatter(
                x=learning_df["Average_Confidence"],
                y=learning_df["Winrate"],
                mode="markers+text",
                text=learning_df["Strategy"],
                textposition="top center",
                name="Confidence",
            )
        )

        conf_fig.update_layout(
            height=500,
            template="plotly_dark",
            title="Confidence vs Winrate",
            xaxis_title="Average Confidence",
            yaxis_title="Winrate",
        )

        st.plotly_chart(
            conf_fig,
            use_container_width=True,
        )

    # ======================================
    # VALIDATION ENGINE
    # ======================================

    st.subheader("🛡️ Strategy Validation")

    validation_input = []

    for trade in journal_data:

        result = str(
            trade.get(
                "result",
                "",
            )
        )

        pnl = 0

        if "+" in result:

            pnl = 1

        elif "-" in result:

            pnl = -1

        validation_input.append(
            {
                "market_regime": trade.get(
                    "market_regime",
                    "UNKNOWN",
                ),
                "strategy": trade.get(
                    "strategy",
                    "UNKNOWN",
                ),
                "profit_loss": pnl,
            }
        )

    validation_df = validate_strategy_by_regime(validation_input)

    if not validation_df.empty:

        st.dataframe(
            validation_df,
            use_container_width=True,
        )

    else:

        st.warning("Validation analysis unavailable")

    # ======================================
    # VALIDATION SCORE CHART
    # ======================================

    st.subheader("📈 Validation Scores")

    if not validation_df.empty:

        validation_df["Label"] = (
            validation_df["Strategy"] + " | " + validation_df["Market_Regime"]
        )

        validation_fig = go.Figure()

        validation_fig.add_trace(
            go.Bar(
                x=validation_df["Label"],
                y=validation_df["Validation_Score"],
                name="Validation",
            )
        )

        validation_fig.update_layout(
            height=500,
            template="plotly_dark",
            title="Validation Score Analysis",
        )

        st.plotly_chart(
            validation_fig,
            use_container_width=True,
        )

    # ======================================
    # JOURNAL VIEWER
    # ======================================

    st.subheader("📋 Trade Journal")

    journal_df = pd.DataFrame(journal_data)

    if not journal_df.empty:

        st.dataframe(
            journal_df,
            use_container_width=True,
        )

    # ======================================
    # EMOTION ANALYSIS
    # ======================================

    st.subheader("😊 Emotion Analysis")

    if not journal_df.empty and "emotion" in journal_df.columns:

        emotion_count = journal_df["emotion"].value_counts().reset_index()

        emotion_count.columns = [
            "Emotion",
            "Count",
        ]

        emotion_fig = go.Figure()

        emotion_fig.add_trace(
            go.Pie(
                labels=emotion_count["Emotion"],
                values=emotion_count["Count"],
                hole=0.4,
            )
        )

        emotion_fig.update_layout(
            height=450,
            template="plotly_dark",
            title="Trading Emotion Distribution",
        )

        st.plotly_chart(
            emotion_fig,
            use_container_width=True,
        )

    # ======================================
    # AI INSIGHTS
    # ======================================

    st.subheader("🧠 AI Insights")

    if not learning_df.empty:

        for _, row in learning_df.iterrows():

            insight = row.get(
                "AI_Insight",
                "",
            )

            st.info(insight)

    # ======================================
    # EXPORT DATA
    # ======================================

    st.subheader("💾 Export Learning Data")

    csv = journal_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Journal CSV",
        data=csv,
        file_name="trade_journal.csv",
        mime="text/csv",
    )

    # ======================================
    # RAW DATA
    # ======================================

    with st.expander("📦 Raw Journal Data"):

        st.json(journal_data)
