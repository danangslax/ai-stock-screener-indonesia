import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from trading.paper_trading import (
    load_trades,
)

from analytics.performance_analytics import (
    analyze_performance,
)

from analytics.strategy_analytics import (
    analyze_strategy_performance,
)

from analytics.analytics import (
    generate_equity_curve,
)

# ======================================
# ANALYTICS DASHBOARD PAGE
# ======================================


def render_analytics_dashboard():

    st.header("📊 Analytics Dashboard")

    # ======================================
    # LOAD TRADES
    # ======================================

    trades = load_trades()

    # ======================================
    # VALIDATION
    # ======================================

    if not trades:

        st.warning("No analytics data available")

        return

    # ======================================
    # PERFORMANCE ANALYTICS
    # ======================================

    performance = analyze_performance(trades)

    # ======================================
    # PERFORMANCE METRICS
    # ======================================

    st.subheader("📈 Performance Metrics")

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "Total Trades",
            performance.get(
                "total_trades",
                0,
            ),
        )

    with m2:

        st.metric(
            "Winrate",
            f"{performance.get('winrate', 0)}%",
        )

    with m3:

        st.metric(
            "Profit Factor",
            performance.get(
                "profit_factor",
                0,
            ),
        )

    with m4:

        st.metric(
            "Sharpe Ratio",
            performance.get(
                "sharpe_ratio",
                0,
            ),
        )

    # ======================================
    # ADDITIONAL METRICS
    # ======================================

    a1, a2, a3, a4 = st.columns(4)

    with a1:

        st.metric(
            "Average Gain",
            performance.get(
                "average_gain",
                0,
            ),
        )

    with a2:

        st.metric(
            "Average Loss",
            performance.get(
                "average_loss",
                0,
            ),
        )

    with a3:

        st.metric(
            "Expectancy",
            performance.get(
                "expectancy",
                0,
            ),
        )

    with a4:

        st.metric(
            "Max Drawdown",
            performance.get(
                "max_drawdown",
                0,
            ),
        )

    # ======================================
    # EQUITY CURVE
    # ======================================

    st.subheader("📈 Equity Curve")

    equity_df = generate_equity_curve(trades)

    if not equity_df.empty:

        equity_fig = go.Figure()

        equity_fig.add_trace(
            go.Scatter(
                x=equity_df.index,
                y=equity_df["equity"],
                mode="lines",
                name="Equity",
            )
        )

        equity_fig.update_layout(
            height=500,
            template="plotly_dark",
            title="Equity Curve",
        )

        st.plotly_chart(
            equity_fig,
            use_container_width=True,
        )

    else:

        st.warning("Equity curve unavailable")

    # ======================================
    # PNL DISTRIBUTION
    # ======================================

    st.subheader("💰 PnL Distribution")

    trades_df = pd.DataFrame(trades)

    if "profit_loss" in trades_df.columns:

        pnl_fig = go.Figure()

        pnl_fig.add_trace(
            go.Histogram(
                x=trades_df["profit_loss"],
                nbinsx=25,
                name="PnL",
            )
        )

        pnl_fig.update_layout(
            height=450,
            template="plotly_dark",
            title="Profit & Loss Distribution",
        )

        st.plotly_chart(
            pnl_fig,
            use_container_width=True,
        )

    # ======================================
    # WIN / LOSS ANALYSIS
    # ======================================

    st.subheader("🏆 Win / Loss Analysis")

    if "profit_loss" in trades_df.columns:

        wins = len(trades_df[trades_df["profit_loss"] > 0])

        losses = len(trades_df[trades_df["profit_loss"] <= 0])

        pie_fig = go.Figure()

        pie_fig.add_trace(
            go.Pie(
                labels=[
                    "Wins",
                    "Losses",
                ],
                values=[
                    wins,
                    losses,
                ],
                hole=0.4,
            )
        )

        pie_fig.update_layout(
            height=450,
            template="plotly_dark",
            title="Win / Loss Ratio",
        )

        st.plotly_chart(
            pie_fig,
            use_container_width=True,
        )

    # ======================================
    # STRATEGY ANALYTICS
    # ======================================

    st.subheader("🎯 Strategy Analytics")

    # ======================================
    # PREPARE DATA
    # ======================================

    strategy_input = []

    for trade in trades:

        if "strategy" in trade and "profit_loss" in trade:

            strategy_input.append(
                {
                    "strategy": trade.get(
                        "strategy",
                        "UNKNOWN",
                    ),
                    "pnl": trade.get(
                        "profit_loss",
                        0,
                    ),
                }
            )

    strategy_df = analyze_strategy_performance(strategy_input)

    if not strategy_df.empty:

        st.dataframe(
            strategy_df,
            use_container_width=True,
        )

        # ======================================
        # STRATEGY PNL CHART
        # ======================================

        strategy_fig = go.Figure()

        strategy_fig.add_trace(
            go.Bar(
                x=strategy_df["strategy"],
                y=strategy_df["Total_PnL"],
                name="Strategy PnL",
            )
        )

        strategy_fig.update_layout(
            height=450,
            template="plotly_dark",
            title="Strategy Performance",
        )

        st.plotly_chart(
            strategy_fig,
            use_container_width=True,
        )

    else:

        st.warning("No strategy analytics available")

    # ======================================
    # TRADE HISTORY
    # ======================================

    st.subheader("📋 Trade History")

    history_df = pd.DataFrame(trades)

    if not history_df.empty:

        # ======================================
        # CLEAN NUMERIC
        # ======================================

        numeric_columns = history_df.select_dtypes(include=["float", "int"]).columns

        history_df[numeric_columns] = history_df[numeric_columns].round(2)

        st.dataframe(
            history_df,
            use_container_width=True,
        )

    # ======================================
    # TOP WINNERS
    # ======================================

    st.subheader("🚀 Top Winners")

    if "profit_loss" in trades_df.columns:

        winners_df = (
            trades_df.sort_values(
                by="profit_loss",
                ascending=False,
            )
            .head(10)
            .copy()
        )

        if not winners_df.empty:

            st.dataframe(
                winners_df,
                use_container_width=True,
            )

    # ======================================
    # TOP LOSERS
    # ======================================

    st.subheader("❌ Top Losers")

    if "profit_loss" in trades_df.columns:

        losers_df = (
            trades_df.sort_values(
                by="profit_loss",
                ascending=True,
            )
            .head(10)
            .copy()
        )

        if not losers_df.empty:

            st.dataframe(
                losers_df,
                use_container_width=True,
            )

    # ======================================
    # MONTHLY PERFORMANCE
    # ======================================

    st.subheader("📅 Monthly Performance")

    if "created_at" in trades_df.columns and "profit_loss" in trades_df.columns:

        try:

            monthly_df = trades_df.copy()

            monthly_df["created_at"] = pd.to_datetime(
                monthly_df["created_at"],
                errors="coerce",
            )

            monthly_df["month"] = monthly_df["created_at"].dt.strftime("%Y-%m")

            grouped_monthly = (
                monthly_df.groupby("month")["profit_loss"].sum().reset_index()
            )

            month_fig = go.Figure()

            month_fig.add_trace(
                go.Bar(
                    x=grouped_monthly["month"],
                    y=grouped_monthly["profit_loss"],
                    name="Monthly PnL",
                )
            )

            month_fig.update_layout(
                height=450,
                template="plotly_dark",
                title="Monthly Profit & Loss",
            )

            st.plotly_chart(
                month_fig,
                use_container_width=True,
            )

        except Exception as e:

            st.error(f"Monthly analytics error: {e}")

    # ======================================
    # EXPORT ANALYTICS
    # ======================================

    st.subheader("💾 Export Analytics")

    export_df = pd.DataFrame(
        [
            {
                "Metric": "Total Trades",
                "Value": performance.get(
                    "total_trades",
                    0,
                ),
            },
            {
                "Metric": "Winrate",
                "Value": performance.get(
                    "winrate",
                    0,
                ),
            },
            {
                "Metric": "Profit Factor",
                "Value": performance.get(
                    "profit_factor",
                    0,
                ),
            },
            {
                "Metric": "Sharpe Ratio",
                "Value": performance.get(
                    "sharpe_ratio",
                    0,
                ),
            },
            {
                "Metric": "Expectancy",
                "Value": performance.get(
                    "expectancy",
                    0,
                ),
            },
            {
                "Metric": "Max Drawdown",
                "Value": performance.get(
                    "max_drawdown",
                    0,
                ),
            },
        ]
    )

    csv = export_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Analytics CSV",
        data=csv,
        file_name="analytics_report.csv",
        mime="text/csv",
    )

    # ======================================
    # RAW DATA
    # ======================================

    with st.expander("📦 Raw Performance Data"):

        st.json(performance)
