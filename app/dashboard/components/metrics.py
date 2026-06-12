import streamlit as st

# ======================================
# PERFORMANCE METRICS
# ======================================


def render_performance_metrics(
    performance,
):

    try:

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

    except Exception as e:

        st.error(f"Performance metric error: {e}")


# ======================================
# MARKET SNAPSHOT METRICS
# ======================================


def render_market_metrics(
    snapshot,
):

    try:

        if not snapshot:

            st.warning("Market snapshot unavailable")

            return

        st.subheader("🌍 Market Metrics")

        m1, m2, m3, m4 = st.columns(4)

        with m1:

            st.metric(
                "Market Status",
                snapshot.get(
                    "market_status",
                    "UNKNOWN",
                ),
            )

        with m2:

            st.metric(
                "Breadth Score",
                snapshot.get(
                    "breadth_score",
                    0,
                ),
            )

        with m3:

            st.metric(
                "Strongest Sector",
                snapshot.get(
                    "strongest_sector",
                    "N/A",
                ),
            )

        with m4:

            st.metric(
                "Market Bias",
                snapshot.get(
                    "market_bias",
                    "UNKNOWN",
                ),
            )

    except Exception as e:

        st.error(f"Market metric error: {e}")


# ======================================
# PORTFOLIO METRICS
# ======================================


def render_portfolio_metrics(
    portfolio,
):

    try:

        st.subheader("💼 Portfolio Metrics")

        m1, m2, m3 = st.columns(3)

        with m1:

            st.metric(
                "Total Positions",
                portfolio.get(
                    "total_positions",
                    0,
                ),
            )

        with m2:

            st.metric(
                "Total Exposure",
                portfolio.get(
                    "total_exposure",
                    0,
                ),
            )

        with m3:

            st.metric(
                "Risk Status",
                portfolio.get(
                    "risk_status",
                    "UNKNOWN",
                ),
            )

    except Exception as e:

        st.error(f"Portfolio metric error: {e}")


# ======================================
# BACKTEST METRICS
# ======================================


def render_backtest_metrics(
    stats,
):

    try:

        st.subheader("🧪 Backtest Metrics")

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

    except Exception as e:

        st.error(f"Backtest metric error: {e}")


# ======================================
# SYSTEM HEALTH METRICS
# ======================================


def render_system_health_metrics(
    cpu_usage,
    memory_usage,
    disk_usage,
):

    try:

        st.subheader("🛠️ System Health")

        m1, m2, m3 = st.columns(3)

        with m1:

            st.metric(
                "CPU Usage",
                f"{cpu_usage}%",
            )

        with m2:

            st.metric(
                "Memory Usage",
                f"{memory_usage}%",
            )

        with m3:

            st.metric(
                "Disk Usage",
                f"{disk_usage}%",
            )

    except Exception as e:

        st.error(f"System metric error: {e}")


# ======================================
# FORWARD TEST METRICS
# ======================================


def render_forward_testing_metrics(
    analytics,
):

    try:

        st.subheader("🧪 Forward Testing Metrics")

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

    except Exception as e:

        st.error(f"Forward metric error: {e}")


# ======================================
# LEARNING METRICS
# ======================================


def render_learning_metrics(
    total_entries,
    high_confidence,
    winrate,
):

    try:

        st.subheader("🧠 Learning Metrics")

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

    except Exception as e:

        st.error(f"Learning metric error: {e}")


# ======================================
# SIMPLE METRIC CARD
# ======================================


def render_metric_card(
    label,
    value,
    delta=None,
):

    try:

        st.metric(
            label=label,
            value=value,
            delta=delta,
        )

    except Exception as e:

        st.error(f"Metric card error: {e}")
