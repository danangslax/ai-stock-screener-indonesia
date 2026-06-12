import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from trading.paper_trading import (
    load_trades,
    load_open_trades,
    load_closed_trades,
)

from portfolio.portfolio_manager import (
    analyze_portfolio,
)

from analytics.analytics import (
    calculate_portfolio_metrics,
    generate_equity_curve,
)

# ======================================
# PORTFOLIO DASHBOARD PAGE
# ======================================


def render_portfolio_dashboard():

    st.header("💼 Portfolio Dashboard")

    # ======================================
    # LOAD TRADES
    # ======================================

    trades = load_trades()

    open_trades = load_open_trades()

    closed_trades = load_closed_trades()

    # ======================================
    # VALIDATION
    # ======================================

    if not trades:

        st.warning("No portfolio data available")

        return

    # ======================================
    # PORTFOLIO ANALYTICS
    # ======================================

    metrics = calculate_portfolio_metrics(trades)

    portfolio = analyze_portfolio(open_trades)

    # ======================================
    # PORTFOLIO METRICS
    # ======================================

    st.subheader("📊 Portfolio Metrics")

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "Total Trades",
            metrics["total_trades"],
        )

    with m2:

        st.metric(
            "Winrate",
            f"{metrics['winrate']}%",
        )

    with m3:

        st.metric(
            "Total PnL",
            round(metrics["total_pnl"], 2),
        )

    with m4:

        st.metric(
            "Profit Factor",
            metrics["profit_factor"],
        )

    # ======================================
    # ADDITIONAL METRICS
    # ======================================

    a1, a2, a3, a4 = st.columns(4)

    with a1:

        st.metric(
            "Open Trades",
            metrics["open_trades"],
        )

    with a2:

        st.metric(
            "Closed Trades",
            metrics["closed_trades"],
        )

    with a3:

        st.metric(
            "Average PnL",
            metrics["average_pnl"],
        )

    with a4:

        st.metric(
            "Expectancy",
            metrics["expectancy"],
        )

    # ======================================
    # PORTFOLIO RISK
    # ======================================

    st.subheader("⚠️ Portfolio Risk")

    r1, r2, r3 = st.columns(3)

    with r1:

        st.metric(
            "Total Exposure",
            round(
                portfolio["total_exposure"],
                2,
            ),
        )

    with r2:

        st.metric(
            "Positions",
            portfolio["total_positions"],
        )

    with r3:

        st.metric(
            "Risk Status",
            portfolio["risk_status"],
        )

    # ======================================
    # SECTOR EXPOSURE
    # ======================================

    st.subheader("🏭 Sector Exposure")

    sector_exposure = portfolio.get(
        "sector_exposure",
        {},
    )

    if sector_exposure:

        sector_df = pd.DataFrame(
            {
                "Sector": list(sector_exposure.keys()),
                "Exposure": list(sector_exposure.values()),
            }
        )

        sector_fig = go.Figure()

        sector_fig.add_trace(
            go.Pie(
                labels=sector_df["Sector"],
                values=sector_df["Exposure"],
                hole=0.4,
            )
        )

        sector_fig.update_layout(
            height=450,
            template="plotly_dark",
            title="Sector Exposure",
        )

        st.plotly_chart(
            sector_fig,
            use_container_width=True,
        )

        st.dataframe(
            sector_df,
            use_container_width=True,
        )

    else:

        st.info("No sector exposure data")

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
            height=450,
            template="plotly_dark",
            title="Portfolio Equity Curve",
        )

        st.plotly_chart(
            equity_fig,
            use_container_width=True,
        )

    else:

        st.warning("No equity curve available")

    # ======================================
    # OPEN TRADES
    # ======================================

    st.subheader("📂 Open Trades")

    if open_trades:

        open_df = pd.DataFrame(open_trades)

        preferred_columns = [
            "symbol",
            "buy_price",
            "quantity",
            "stop_loss",
            "take_profit",
            "position_value",
            "strategy",
            "market_regime",
            "status",
        ]

        available_columns = [col for col in preferred_columns if col in open_df.columns]

        display_open_df = open_df[available_columns].copy()

        numeric_columns = display_open_df.select_dtypes(
            include=["float", "int"]
        ).columns

        display_open_df[numeric_columns] = display_open_df[numeric_columns].round(2)

        st.dataframe(
            display_open_df,
            use_container_width=True,
        )

    else:

        st.info("No open trades")

    # ======================================
    # CLOSED TRADES
    # ======================================

    st.subheader("✅ Closed Trades")

    if closed_trades:

        closed_df = pd.DataFrame(closed_trades)

        preferred_columns = [
            "symbol",
            "buy_price",
            "sell_price",
            "quantity",
            "profit_loss",
            "profit_loss_percent",
            "result",
            "strategy",
            "close_reason",
        ]

        available_columns = [
            col for col in preferred_columns if col in closed_df.columns
        ]

        display_closed_df = closed_df[available_columns].copy()

        numeric_columns = display_closed_df.select_dtypes(
            include=["float", "int"]
        ).columns

        display_closed_df[numeric_columns] = display_closed_df[numeric_columns].round(2)

        st.dataframe(
            display_closed_df,
            use_container_width=True,
        )

    else:

        st.info("No closed trades")

    # ======================================
    # PNL DISTRIBUTION
    # ======================================

    st.subheader("💰 PnL Distribution")

    if closed_trades:

        pnl_df = pd.DataFrame(closed_trades)

        if "profit_loss" in pnl_df.columns:

            pnl_fig = go.Figure()

            pnl_fig.add_trace(
                go.Bar(
                    x=pnl_df.index,
                    y=pnl_df["profit_loss"],
                    name="PnL",
                )
            )

            pnl_fig.update_layout(
                height=400,
                template="plotly_dark",
                title="Trade PnL Distribution",
            )

            st.plotly_chart(
                pnl_fig,
                use_container_width=True,
            )

    # ======================================
    # PERFORMANCE SUMMARY
    # ======================================

    st.subheader("🧠 Portfolio Insight")

    insight = f"""
Portfolio Overview

Total Trades:
{metrics['total_trades']}

Winning Trades:
{metrics['winning_trades']}

Losing Trades:
{metrics['losing_trades']}

Winrate:
{metrics['winrate']}%

Profit Factor:
{metrics['profit_factor']}

Expectancy:
{metrics['expectancy']}

Risk Status:
{portfolio['risk_status']}

Total Exposure:
{round(portfolio['total_exposure'], 2)}
"""

    st.info(insight)

    # ======================================
    # EXPORT SECTION
    # ======================================

    st.subheader("💾 Export Portfolio")

    trades_df = pd.DataFrame(trades)

    csv = trades_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Portfolio CSV",
        data=csv,
        file_name="portfolio_data.csv",
        mime="text/csv",
    )

    # ======================================
    # RAW DATA
    # ======================================

    with st.expander("📦 Raw Portfolio Data"):

        st.dataframe(
            trades_df,
            use_container_width=True,
        )
