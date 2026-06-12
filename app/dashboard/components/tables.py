import streamlit as st
import pandas as pd

# ======================================
# GENERIC DATAFRAME TABLE
# ======================================


def render_dataframe_table(
    df,
    title="Data Table",
    height=400,
):

    try:

        st.subheader(title)

        if df is None:

            st.warning("No data available")

            return

        if isinstance(df, pd.DataFrame):

            if df.empty:

                st.warning("Empty dataframe")

                return

            st.dataframe(
                df,
                use_container_width=True,
                height=height,
            )

            return

        st.warning("Invalid dataframe")

    except Exception as e:

        st.error(f"Table render error: {e}")


# ======================================
# SCREENER TABLE
# ======================================


def render_screener_table(
    screener_df,
):

    try:

        st.subheader("🔥 AI Screener Results")

        if screener_df is None or screener_df.empty:

            st.warning("No screener results")

            return

        preferred_columns = [
            "Symbol",
            "Price",
            "Score",
            "Confidence",
            "Strategy",
            "Market",
            "RSI",
            "ADX",
            "Relative_Strength",
        ]

        available_columns = [
            col for col in preferred_columns if col in screener_df.columns
        ]

        if available_columns:

            st.dataframe(
                screener_df[available_columns],
                use_container_width=True,
                height=500,
            )

        else:

            st.dataframe(
                screener_df,
                use_container_width=True,
                height=500,
            )

    except Exception as e:

        st.error(f"Screener table error: {e}")


# ======================================
# PORTFOLIO TABLE
# ======================================


def render_portfolio_table(
    trades_df,
):

    try:

        st.subheader("💼 Portfolio Positions")

        if trades_df is None or trades_df.empty:

            st.warning("No portfolio data")

            return

        preferred_columns = [
            "symbol",
            "buy_price",
            "quantity",
            "status",
            "profit_loss",
            "strategy",
            "market_regime",
        ]

        available_columns = [
            col for col in preferred_columns if col in trades_df.columns
        ]

        if available_columns:

            st.dataframe(
                trades_df[available_columns],
                use_container_width=True,
                height=450,
            )

        else:

            st.dataframe(
                trades_df,
                use_container_width=True,
                height=450,
            )

    except Exception as e:

        st.error(f"Portfolio table error: {e}")


# ======================================
# STRATEGY ANALYTICS TABLE
# ======================================


def render_strategy_table(
    strategy_df,
):

    try:

        st.subheader("🎯 Strategy Analytics")

        if strategy_df is None or strategy_df.empty:

            st.warning("No strategy analytics")

            return

        st.dataframe(
            strategy_df,
            use_container_width=True,
            height=450,
        )

    except Exception as e:

        st.error(f"Strategy table error: {e}")


# ======================================
# FORWARD TEST TABLE
# ======================================


def render_forward_testing_table(
    df,
):

    try:

        st.subheader("🧪 Forward Testing")

        if df is None or df.empty:

            st.warning("No forward testing data")

            return

        preferred_columns = [
            "date",
            "symbol",
            "price",
            "confidence",
            "strategy",
            "market_regime",
            "forward_return",
            "status",
        ]

        available_columns = [col for col in preferred_columns if col in df.columns]

        if available_columns:

            st.dataframe(
                df[available_columns],
                use_container_width=True,
                height=500,
            )

        else:

            st.dataframe(
                df,
                use_container_width=True,
                height=500,
            )

    except Exception as e:

        st.error(f"Forward testing table error: {e}")


# ======================================
# LEARNING TABLE
# ======================================


def render_learning_table(
    learning_df,
):

    try:

        st.subheader("🧠 AI Learning Results")

        if learning_df is None or learning_df.empty:

            st.warning("No learning data")

            return

        st.dataframe(
            learning_df,
            use_container_width=True,
            height=500,
        )

    except Exception as e:

        st.error(f"Learning table error: {e}")


# ======================================
# MARKET SNAPSHOT TABLE
# ======================================


def render_market_snapshot_table(
    snapshot,
):

    try:

        st.subheader("🌍 Market Snapshot")

        if not snapshot:

            st.warning("No snapshot data")

            return

        snapshot_df = pd.DataFrame(
            [
                {
                    "Metric": key,
                    "Value": value,
                }
                for key, value in snapshot.items()
            ]
        )

        st.dataframe(
            snapshot_df,
            use_container_width=True,
            height=350,
        )

    except Exception as e:

        st.error(f"Snapshot table error: {e}")


# ======================================
# PERFORMANCE TABLE
# ======================================


def render_performance_table(
    performance,
):

    try:

        st.subheader("📈 Performance Summary")

        if not performance:

            st.warning("No performance data")

            return

        performance_df = pd.DataFrame(
            [
                {
                    "Metric": key,
                    "Value": value,
                }
                for key, value in performance.items()
            ]
        )

        st.dataframe(
            performance_df,
            use_container_width=True,
            height=400,
        )

    except Exception as e:

        st.error(f"Performance table error: {e}")


# ======================================
# BACKTEST TABLE
# ======================================


def render_backtest_table(
    stats,
):

    try:

        st.subheader("🧪 Backtest Results")

        if stats is None:

            st.warning("No backtest results")

            return

        stats_dict = dict(stats)

        stats_df = pd.DataFrame(
            [
                {
                    "Metric": key,
                    "Value": value,
                }
                for key, value in stats_dict.items()
            ]
        )

        st.dataframe(
            stats_df,
            use_container_width=True,
            height=500,
        )

    except Exception as e:

        st.error(f"Backtest table error: {e}")


# ======================================
# OPEN TRADES TABLE
# ======================================


def render_open_trades_table(
    trades,
):

    try:

        st.subheader("📂 Open Trades")

        if not trades:

            st.warning("No open trades")

            return

        df = pd.DataFrame(trades)

        st.dataframe(
            df,
            use_container_width=True,
            height=450,
        )

    except Exception as e:

        st.error(f"Open trades table error: {e}")


# ======================================
# CLOSED TRADES TABLE
# ======================================


def render_closed_trades_table(
    trades,
):

    try:

        st.subheader("✅ Closed Trades")

        if not trades:

            st.warning("No closed trades")

            return

        df = pd.DataFrame(trades)

        st.dataframe(
            df,
            use_container_width=True,
            height=450,
        )

    except Exception as e:

        st.error(f"Closed trades table error: {e}")


# ======================================
# SYSTEM HEALTH TABLE
# ======================================


def render_system_health_table(
    health_data,
):

    try:

        st.subheader("🛠️ System Health")

        if not health_data:

            st.warning("No health data")

            return

        df = pd.DataFrame(
            [
                {
                    "Component": key,
                    "Status": value,
                }
                for key, value in health_data.items()
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            height=350,
        )

    except Exception as e:

        st.error(f"System health table error: {e}")
