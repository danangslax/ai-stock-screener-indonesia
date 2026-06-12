import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from storage.forward_storage import (
    load_forward_signals,
)

from ai.forward_testing import (
    analyze_forward_testing,
)

# ======================================
# FORWARD TESTING DASHBOARD PAGE
# ======================================


def render_forward_testing_dashboard():

    st.header("🧪 Forward Testing Dashboard")

    # ======================================
    # LOAD SIGNALS
    # ======================================

    signals = load_forward_signals()

    # ======================================
    # VALIDATION
    # ======================================

    if not signals:

        st.warning("No forward testing data available")

        return

    # ======================================
    # ANALYZE PERFORMANCE
    # ======================================

    analytics = analyze_forward_testing(signals)

    # ======================================
    # METRICS
    # ======================================

    st.subheader("📊 Forward Testing Metrics")

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "Total Signals",
            analytics.get(
                "total_signals",
                0,
            ),
        )

    with m2:

        st.metric(
            "Winrate",
            f"{analytics.get('winrate', 0)}%",
        )

    with m3:

        st.metric(
            "Average Return",
            f"{analytics.get('average_return', 0)}%",
        )

    with m4:

        st.metric(
            "High Confidence Return",
            f"{analytics.get('high_confidence_return', 0)}%",
        )

    # ======================================
    # DATAFRAME
    # ======================================

    st.subheader("📋 Forward Signals")

    df = pd.DataFrame(signals)

    if not df.empty:

        # ======================================
        # CLEAN NUMERIC
        # ======================================

        numeric_columns = df.select_dtypes(include=["float", "int"]).columns

        df[numeric_columns] = df[numeric_columns].round(2)

        st.dataframe(
            df,
            use_container_width=True,
        )

    # ======================================
    # RETURN DISTRIBUTION
    # ======================================

    st.subheader("💰 Forward Return Distribution")

    if not df.empty and "forward_return" in df.columns:

        hist_fig = go.Figure()

        hist_fig.add_trace(
            go.Histogram(
                x=df["forward_return"],
                nbinsx=20,
                name="Returns",
            )
        )

        hist_fig.update_layout(
            height=450,
            template="plotly_dark",
            title="Forward Return Distribution",
        )

        st.plotly_chart(
            hist_fig,
            use_container_width=True,
        )

    # ======================================
    # CONFIDENCE VS RETURN
    # ======================================

    st.subheader("⚡ Confidence vs Return")

    if not df.empty and "confidence" in df.columns and "forward_return" in df.columns:

        scatter_fig = go.Figure()

        scatter_fig.add_trace(
            go.Scatter(
                x=df["confidence"],
                y=df["forward_return"],
                mode="markers+text",
                text=df["symbol"],
                textposition="top center",
                name="Signals",
            )
        )

        scatter_fig.update_layout(
            height=500,
            template="plotly_dark",
            title="Confidence vs Forward Return",
            xaxis_title="Confidence",
            yaxis_title="Forward Return %",
        )

        st.plotly_chart(
            scatter_fig,
            use_container_width=True,
        )

    # ======================================
    # STRATEGY ANALYSIS
    # ======================================

    st.subheader("🎯 Strategy Performance")

    if not df.empty and "strategy" in df.columns:

        strategy_df = (
            df.groupby("strategy")
            .agg(
                {
                    "forward_return": [
                        "mean",
                        "count",
                    ]
                }
            )
            .reset_index()
        )

        strategy_df.columns = [
            "Strategy",
            "Average_Return",
            "Total_Signals",
        ]

        strategy_df["Average_Return"] = strategy_df["Average_Return"].round(2)

        st.dataframe(
            strategy_df,
            use_container_width=True,
        )

        # ======================================
        # STRATEGY CHART
        # ======================================

        strategy_fig = go.Figure()

        strategy_fig.add_trace(
            go.Bar(
                x=strategy_df["Strategy"],
                y=strategy_df["Average_Return"],
                name="Strategy Return",
            )
        )

        strategy_fig.update_layout(
            height=450,
            template="plotly_dark",
            title="Average Return by Strategy",
        )

        st.plotly_chart(
            strategy_fig,
            use_container_width=True,
        )

    # ======================================
    # MARKET REGIME ANALYSIS
    # ======================================

    st.subheader("🌍 Market Regime Analysis")

    if not df.empty and "market_regime" in df.columns:

        regime_df = (
            df.groupby("market_regime")
            .agg(
                {
                    "forward_return": [
                        "mean",
                        "count",
                    ]
                }
            )
            .reset_index()
        )

        regime_df.columns = [
            "Market_Regime",
            "Average_Return",
            "Total_Signals",
        ]

        regime_df["Average_Return"] = regime_df["Average_Return"].round(2)

        st.dataframe(
            regime_df,
            use_container_width=True,
        )

        # ======================================
        # REGIME CHART
        # ======================================

        regime_fig = go.Figure()

        regime_fig.add_trace(
            go.Bar(
                x=regime_df["Market_Regime"],
                y=regime_df["Average_Return"],
                name="Regime Return",
            )
        )

        regime_fig.update_layout(
            height=450,
            template="plotly_dark",
            title="Market Regime Performance",
        )

        st.plotly_chart(
            regime_fig,
            use_container_width=True,
        )

    # ======================================
    # STATUS ANALYSIS
    # ======================================

    st.subheader("📌 Signal Status")

    if not df.empty and "status" in df.columns:

        status_count = df["status"].value_counts().reset_index()

        status_count.columns = [
            "Status",
            "Count",
        ]

        status_fig = go.Figure()

        status_fig.add_trace(
            go.Pie(
                labels=status_count["Status"],
                values=status_count["Count"],
                hole=0.4,
            )
        )

        status_fig.update_layout(
            height=450,
            template="plotly_dark",
            title="Signal Status Distribution",
        )

        st.plotly_chart(
            status_fig,
            use_container_width=True,
        )

    # ======================================
    # HIGH CONFIDENCE SIGNALS
    # ======================================

    st.subheader("🚀 High Confidence Signals")

    if not df.empty and "confidence" in df.columns:

        high_conf_df = df[df["confidence"] >= 80].copy()

        if not high_conf_df.empty:

            st.dataframe(
                high_conf_df,
                use_container_width=True,
            )

        else:

            st.warning("No high confidence signals found")

    # ======================================
    # BEST SIGNALS
    # ======================================

    st.subheader("🏆 Best Performing Signals")

    if not df.empty and "forward_return" in df.columns:

        best_df = (
            df.sort_values(
                by="forward_return",
                ascending=False,
            )
            .head(10)
            .copy()
        )

        st.dataframe(
            best_df,
            use_container_width=True,
        )

    # ======================================
    # WORST SIGNALS
    # ======================================

    st.subheader("❌ Worst Performing Signals")

    if not df.empty and "forward_return" in df.columns:

        worst_df = (
            df.sort_values(
                by="forward_return",
                ascending=True,
            )
            .head(10)
            .copy()
        )

        st.dataframe(
            worst_df,
            use_container_width=True,
        )

    # ======================================
    # EXPORT DATA
    # ======================================

    st.subheader("💾 Export Forward Testing")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Forward Testing CSV",
        data=csv,
        file_name="forward_testing.csv",
        mime="text/csv",
    )

    # ======================================
    # RAW ANALYTICS
    # ======================================

    with st.expander("📦 Raw Analytics"):

        st.json(analytics)
