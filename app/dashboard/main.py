import sys

from pathlib import Path

# ======================================
# ROOT PATH FIX
# ======================================

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

if str(ROOT_DIR) not in sys.path:

    sys.path.append(str(ROOT_DIR))

# ======================================
# IMPORTS
# ======================================

import streamlit as st

from app.dashboard.pages.stock_overview import render_stock_overview

from app.dashboard.pages.market_snapshot import render_market_snapshot

from app.dashboard.pages.screener_dashboard import render_screener_dashboard

from app.dashboard.pages.portfolio_dashboard import render_portfolio_dashboard

from app.dashboard.pages.analytics_dashboard import render_analytics_dashboard

from app.dashboard.pages.backtest_dashboard import render_backtest_dashboard

from app.dashboard.pages.ai_learning_dashboard import render_ai_learning_dashboard

from app.dashboard.pages.system_health_dashboard import render_system_health_dashboard

from infrastructure.logger import logger

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(page_title="AI Stock Screener Indonesia", layout="wide")

# ======================================
# APPLICATION TITLE
# ======================================

st.title("📈 AI Stock Screener Indonesia")

st.caption("Institutional Grade AI Swing Trading System")

# ======================================
# SIDEBAR
# ======================================

st.sidebar.title("⚙️ Dashboard Navigation")

dashboard_mode = st.sidebar.radio(
    "Select Module",
    [
        "Stock Overview",
        "Market Snapshot",
        "AI Screener",
        "Portfolio",
        "Analytics",
        "Backtest",
        "AI Learning",
        "System Health",
    ],
)

# ======================================
# LOG START
# ======================================

logger.info(f"Dashboard Loaded: " f"{dashboard_mode}")

# ======================================
# STOCK OVERVIEW
# ======================================

if dashboard_mode == "Stock Overview":

    try:

        render_stock_overview()

    except Exception as e:

        st.error(f"Stock Overview Error: {e}")

        logger.error(f"Stock Overview Error: {e}")

# ======================================
# MARKET SNAPSHOT
# ======================================

elif dashboard_mode == "Market Snapshot":

    try:

        render_market_snapshot()

    except Exception as e:

        st.error(f"Market Snapshot Error: {e}")

        logger.error(f"Market Snapshot Error: {e}")

# ======================================
# AI SCREENER
# ======================================

elif dashboard_mode == "AI Screener":

    try:

        render_screener_dashboard()

    except Exception as e:

        st.error(f"Screener Dashboard Error: {e}")

        logger.error(f"Screener Dashboard Error: {e}")

# ======================================
# PORTFOLIO
# ======================================

elif dashboard_mode == "Portfolio":

    try:

        render_portfolio_dashboard()

    except Exception as e:

        st.error(f"Portfolio Dashboard Error: {e}")

        logger.error(f"Portfolio Dashboard Error: {e}")

# ======================================
# ANALYTICS
# ======================================

elif dashboard_mode == "Analytics":

    try:

        render_analytics_dashboard()

    except Exception as e:

        st.error(f"Analytics Dashboard Error: {e}")

        logger.error(f"Analytics Dashboard Error: {e}")

# ======================================
# BACKTEST
# ======================================

elif dashboard_mode == "Backtest":

    try:

        render_backtest_dashboard()

    except Exception as e:

        st.error(f"Backtest Dashboard Error: {e}")

        logger.error(f"Backtest Dashboard Error: {e}")

# ======================================
# AI LEARNING
# ======================================

elif dashboard_mode == "AI Learning":

    try:

        render_ai_learning_dashboard()

    except Exception as e:

        st.error(f"AI Learning Dashboard Error: {e}")

        logger.error(f"AI Learning Dashboard Error: {e}")

# ======================================
# SYSTEM HEALTH
# ======================================

elif dashboard_mode == "System Health":

    try:

        render_system_health_dashboard()

    except Exception as e:

        st.error(f"System Health Dashboard Error: {e}")

        logger.error(f"System Health Dashboard Error: {e}")

# ======================================
# FOOTER
# ======================================

st.divider()

st.caption("🤖 AI Stock Screener Indonesia | " "Institutional Swing Trading Framework")
