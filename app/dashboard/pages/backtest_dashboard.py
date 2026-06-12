import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from analytics.backtest import run_backtest

# ======================================
# BACKTEST DASHBOARD PAGE
# ======================================


def render_backtest_dashboard():

    st.header("🧪 Backtest Dashboard")

    # ======================================
    # INPUTS
    # ======================================

    st.subheader("⚙️ Backtest Settings")

    col1, col2, col3 = st.columns(3)

    with col1:

        symbol = st.text_input(
            "Stock Symbol",
            value="BBRI.JK",
        )

    with col2:

        period = st.selectbox(
            "Backtest Period",
            [
                "6mo",
                "1y",
                "2y",
                "5y",
            ],
            index=1,
        )

    with col3:

        starting_capital = st.number_input(
            "Starting Capital",
            min_value=1_000_000,
            value=100_000_000,
            step=1_000_000,
        )

    # ======================================
    # RUN BUTTON
    # ======================================

    run_button = st.button(
        "🚀 Run Backtest",
        use_container_width=True,
    )

    # ======================================
    # RUN ENGINE
    # ======================================

    if run_button:

        with st.spinner("Running backtest..."):

            stats = run_backtest(
                symbol=symbol,
                period=period,
            )

        # ======================================
        # VALIDATION
        # ======================================

        if stats is None:

            st.error("Backtest failed")

            return

        # ======================================
        # HEADER
        # ======================================

        st.success(f"✅ Backtest Completed: {symbol}")

        # ======================================
        # PERFORMANCE METRICS
        # ======================================

        st.subheader("📈 Performance Metrics")

        m1, m2, m3, m4 = st.columns(4)

        with m1:

            st.metric(
                "Return %",
                round(
                    float(
                        stats.get(
                            "Return [%]",
                            0,
                        )
                    ),
                    2,
                ),
            )

        with m2:

            st.metric(
                "Win Rate %",
                round(
                    float(
                        stats.get(
                            "Win Rate [%]",
                            0,
                        )
                    ),
                    2,
                ),
            )

        with m3:

            st.metric(
                "Profit Factor",
                round(
                    float(
                        stats.get(
                            "Profit Factor",
                            0,
                        )
                    ),
                    2,
                ),
            )

        with m4:

            st.metric(
                "Sharpe Ratio",
                round(
                    float(
                        stats.get(
                            "Sharpe Ratio",
                            0,
                        )
                    ),
                    2,
                ),
            )

        # ======================================
        # ADDITIONAL METRICS
        # ======================================

        a1, a2, a3, a4 = st.columns(4)

        with a1:

            st.metric(
                "Total Trades",
                int(
                    stats.get(
                        "# Trades",
                        0,
                    )
                ),
            )

        with a2:

            st.metric(
                "Max Drawdown %",
                round(
                    float(
                        stats.get(
                            "Max. Drawdown [%]",
                            0,
                        )
                    ),
                    2,
                ),
            )

        with a3:

            st.metric(
                "Best Trade %",
                round(
                    float(
                        stats.get(
                            "Best Trade [%]",
                            0,
                        )
                    ),
                    2,
                ),
            )

        with a4:

            st.metric(
                "Worst Trade %",
                round(
                    float(
                        stats.get(
                            "Worst Trade [%]",
                            0,
                        )
                    ),
                    2,
                ),
            )

        # ======================================
        # EQUITY CURVE
        # ======================================

        st.subheader("📊 Equity Curve")

        if "_equity_curve" in stats:

            equity_curve = stats["_equity_curve"]

            if not equity_curve.empty:

                equity_fig = go.Figure()

                equity_fig.add_trace(
                    go.Scatter(
                        x=equity_curve.index,
                        y=equity_curve["Equity"],
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

        # ======================================
        # DRAWDOWN CHART
        # ======================================

        st.subheader("📉 Drawdown Analysis")

        if "_equity_curve" in stats:

            equity_curve = stats["_equity_curve"]

            if not equity_curve.empty and "DrawdownPct" in equity_curve.columns:

                drawdown_fig = go.Figure()

                drawdown_fig.add_trace(
                    go.Scatter(
                        x=equity_curve.index,
                        y=equity_curve["DrawdownPct"],
                        fill="tozeroy",
                        mode="lines",
                        name="Drawdown",
                    )
                )

                drawdown_fig.update_layout(
                    height=400,
                    template="plotly_dark",
                    title="Drawdown Curve",
                )

                st.plotly_chart(
                    drawdown_fig,
                    use_container_width=True,
                )

        # ======================================
        # TRADE ANALYSIS
        # ======================================

        st.subheader("📋 Trade Analysis")

        if "_trades" in stats:

            trades_df = stats["_trades"]

            if not trades_df.empty:

                # ======================================
                # CLEAN DATA
                # ======================================

                display_df = trades_df.copy()

                numeric_columns = display_df.select_dtypes(
                    include=["float", "int"]
                ).columns

                display_df[numeric_columns] = display_df[numeric_columns].round(2)

                st.dataframe(
                    display_df,
                    use_container_width=True,
                )

        # ======================================
        # TRADE PNL CHART
        # ======================================

        st.subheader("💰 Trade PnL")

        if "_trades" in stats:

            trades_df = stats["_trades"]

            if not trades_df.empty and "PnL" in trades_df.columns:

                pnl_fig = go.Figure()

                pnl_fig.add_trace(
                    go.Bar(
                        x=trades_df.index,
                        y=trades_df["PnL"],
                        name="PnL",
                    )
                )

                pnl_fig.update_layout(
                    height=400,
                    template="plotly_dark",
                    title="Trade Profit / Loss",
                )

                st.plotly_chart(
                    pnl_fig,
                    use_container_width=True,
                )

        # ======================================
        # STRATEGY SUMMARY
        # ======================================

        st.subheader("🧠 Strategy Summary")

        summary = f"""
Backtest Summary

Symbol:
{symbol}

Period:
{period}

Total Return:
{round(float(stats.get('Return [%]', 0)), 2)}%

Win Rate:
{round(float(stats.get('Win Rate [%]', 0)), 2)}%

Profit Factor:
{round(float(stats.get('Profit Factor', 0)), 2)}

Sharpe Ratio:
{round(float(stats.get('Sharpe Ratio', 0)), 2)}

Max Drawdown:
{round(float(stats.get('Max. Drawdown [%]', 0)), 2)}%

Total Trades:
{int(stats.get('# Trades', 0))}
"""

        st.info(summary)

        # ======================================
        # RAW STATS
        # ======================================

        st.subheader("📦 Raw Backtest Data")

        raw_stats = {}

        for key, value in stats.items():

            if isinstance(
                value,
                (
                    int,
                    float,
                    str,
                    bool,
                ),
            ):

                raw_stats[key] = value

        raw_df = pd.DataFrame(
            {
                "Metric": list(raw_stats.keys()),
                "Value": list(raw_stats.values()),
            }
        )

        st.dataframe(
            raw_df,
            use_container_width=True,
        )

        # ======================================
        # EXPORT RESULTS
        # ======================================

        st.subheader("💾 Export Backtest")

        csv = raw_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Results CSV",
            data=csv,
            file_name="backtest_results.csv",
            mime="text/csv",
        )
