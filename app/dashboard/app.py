import sys

from pathlib import Path

# ======================================
# ROOT PATH FIX
# ======================================

sys.path.append(str(Path(__file__).resolve().parent.parent))

# ======================================
# IMPORTS
# ======================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from core.data_loader import load_stock_data

from core.trade_plan import generate_trade_plan

from core.snapshot_loader import load_market_snapshot

from database.queries import load_screener_history

from core.paper_trading import create_trade, load_trades

from core.analytics import calculate_portfolio_metrics, generate_equity_curve

from core.backtest import run_backtest

from core.strategy_analytics import analyze_strategy_performance

from core.market_intelligence import generate_market_intelligence

from core.position_sizing import calculate_position_size

from core.portfolio_manager import analyze_portfolio

from core.trade_journal import add_trade_journal, load_journal

from core.learning_engine import analyze_learning_data

from core.walk_forward import optimize_parameters

from core.auto_tuning import auto_tune_parameters

from core.ai_parameters import load_parameters

from core.market_simulator import simulate_market_conditions

from core.cache_validator import validate_all_cache

from core.performance_analytics import analyze_performance

from core.validation_engine import validate_strategy_by_regime

from core.forward_testing import create_forward_signal, analyze_forward_testing

from core.forward_storage import add_forward_signal, load_forward_signals

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(page_title=("AI Stock Screener Indonesia"), layout="wide")

# ======================================
# BASE DIRECTORY
# ======================================

BASE_DIR = Path(__file__).resolve().parent.parent

# ======================================
# WATCHLIST PATH
# ======================================

WATCHLIST_PATH = BASE_DIR / "watchlist" / "idx_stocks.txt"

# ======================================
# TITLE
# ======================================

st.title("📈 AI Stock Screener Indonesia")

# ======================================
# WATCHLIST
# ======================================

st.sidebar.title("📌 Watchlist")

try:

    with open(WATCHLIST_PATH, "r", encoding="utf-8") as f:

        watchlist = [line.strip().replace(".JK", "") for line in f if line.strip()]

except Exception as e:

    st.error(f"Watchlist error: {e}")

    st.stop()

# ======================================
# SELECT WATCHLIST
# ======================================

selected_watchlist = st.sidebar.selectbox("Pilih saham", watchlist)

# ======================================
# INPUT
# ======================================

ticker = st.text_input("Masukkan kode saham IDX", value=selected_watchlist)

symbol = f"{ticker.upper()}.JK"

# ======================================
# LOAD DATA
# ======================================

try:

    df = load_stock_data(symbol, cache_only=True)

except Exception as e:

    st.error(f"Data loading error: {e}")

    st.stop()

# ======================================
# VALIDATION
# ======================================

if df.empty:

    st.error("Data saham tidak ditemukan")

    st.stop()

# ======================================
# VALIDATE ENRICHED CACHE
# ======================================

if "RSI" not in df.columns:

    st.error("Indicators not found in cache")

    st.stop()

# ======================================
# DATA VALIDATION
# ======================================

if len(df) < 2:

    st.warning("Data saham belum cukup")

    st.stop()

# ======================================
# LATEST DATA
# ======================================

latest = df.iloc[-1]

previous = df.iloc[-2]

close_price = float(latest["Close"])

volume = float(latest["Volume"])

change_percent = ((close_price - previous["Close"]) / previous["Close"]) * 100

# ======================================
# STOCK OVERVIEW
# ======================================

st.subheader("📌 Stock Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Last Price", f"Rp {close_price:,.2f}")

col2.metric("Volume", f"{int(volume):,}")

col3.metric("Change %", f"{change_percent:.2f}%")

# ======================================
# TECHNICAL INDICATORS
# ======================================

st.subheader("📊 Technical Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("MA5", f"{latest['MA5']:.2f}")

col2.metric("MA20", f"{latest['MA20']:.2f}")

col3.metric("RSI", f"{latest['RSI']:.2f}")

col4.metric("VOL MA20", f"{int(latest['VOL_MA20']):,}")

# ======================================
# CHART
# ======================================

fig = go.Figure()

# ======================================
# CANDLESTICK
# ======================================

fig.add_trace(
    go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Price",
    )
)

# ======================================
# BOLLINGER BANDS
# ======================================

fig.add_trace(go.Scatter(x=df.index, y=df["BB_UPPER"], name="BB Upper"))

fig.add_trace(go.Scatter(x=df.index, y=df["BB_MIDDLE"], name="BB Middle"))

fig.add_trace(go.Scatter(x=df.index, y=df["BB_LOWER"], name="BB Lower"))

# ======================================
# LAYOUT
# ======================================

fig.update_layout(height=600, xaxis_rangeslider_visible=False)

# ======================================
# SHOW CHART
# ======================================

st.plotly_chart(fig, use_container_width=True)

# ======================================
# HISTORICAL DATA
# ======================================

st.subheader("📜 Historical Data")

st.dataframe(df.tail(20), use_container_width=True)

# ======================================
# REFRESH BUTTON
# ======================================

st.divider()

if st.button("🔄 Refresh Data"):

    st.cache_data.clear()

    st.rerun()

# ======================================
# MARKET SNAPSHOT
# ======================================

st.header("📊 Market Snapshot")

snapshot = load_market_snapshot()

if snapshot:

    intelligence = generate_market_intelligence(snapshot)

    st.info(intelligence)

    st.success(f"""
🌍 Market: {snapshot['market_status']}

📊 Breadth Score:
{snapshot['breadth_score']}

🏭 Strongest Sector:
{snapshot['strongest_sector']}

👑 Sector Leader:
{snapshot['sector_leader']}

🎯 Market Bias:
{snapshot['market_bias']}
""")

else:

    st.warning("Snapshot not available")

# ======================================
# LATEST AI SCREENER
# ======================================

st.divider()

st.header("🔥 Latest AI Screener")

try:

    history = load_screener_history()

except Exception as e:

    st.error(f"Database error: {e}")

    history = []

if history:

    screener_df = pd.DataFrame(history)

    # ======================================
    # TOP PICK
    # ======================================

    top_pick = screener_df.iloc[0]

    st.subheader("🏆 Top Pick")

    col1, col2, col3 = st.columns(3)

    col1.metric("Symbol", top_pick["Symbol"])

    col2.metric("Score", top_pick["Score"])

    col3.metric("RSI", top_pick["RSI"])

# ======================================
# SAVE FORWARD SIGNAL
# ======================================

forward_signal = create_forward_signal(top_pick)

if forward_signal:

    add_forward_signal(forward_signal)

    # ======================================
    # TRADE PLAN
    # ======================================

    trade_plan = generate_trade_plan(top_pick["Price"])

    st.subheader("📌 Trade Plan")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Entry", trade_plan["entry"])

    col2.metric("Stop Loss", trade_plan["stop_loss"])

    col3.metric("Take Profit", trade_plan["take_profit"])

    col4.metric("Risk Reward", trade_plan["risk_reward"])

# ======================================
# POSITION SIZING
# ======================================

st.subheader("💰 Position Sizing")

capital_input = st.number_input(
    "Trading Capital", min_value=1_000_000, value=100_000_000, step=1_000_000
)

risk_input = st.slider("Risk Per Trade (%)", min_value=1, max_value=5, value=1)

position_data = calculate_position_size(
    capital_input, float(top_pick["Price"]), float(top_pick["Stop_Loss"]), risk_input
)

if position_data:

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Recommended Lots", position_data["recommended_lots"])

    col2.metric("Position Value", f"Rp {position_data['position_value']:,.0f}")

    col3.metric("Max Loss", f"Rp {position_data['max_loss']:,.0f}")

    col4.metric("Risk Capital", f"Rp {position_data['risk_capital']:,.0f}")

    # ======================================
    # PAPER TRADING
    # ======================================

    st.subheader("💰 Paper Trading")

    if st.button("📈 Buy Top Pick"):

        try:

            create_trade(
                symbol=(top_pick["Symbol"]),
                buy_price=float(top_pick["Price"]),
                quantity=1,
                strategy=top_pick.get("Strategy", "UNKNOWN"),
            )

            add_trade_journal(
                symbol=top_pick["Symbol"],
                strategy=top_pick.get("Strategy", "UNKNOWN"),
                market_regime=top_pick.get("Market", "UNKNOWN"),
                confidence=top_pick.get("Confidence", 0),
                entry_reason=(f"""
            Weekly:
            {top_pick.get('Weekly_Status')}

            Daily:
            {top_pick.get('Daily_Status')}

            RS:
            {top_pick.get('RS_Status')}
            """),
            )

            st.success("Paper trade berhasil dibuat")

        except Exception as e:

            st.error(f"Trade error: {e}")

    # ======================================
    # RESULT TABLE
    # ======================================

    st.subheader("📊 Latest Screening Results")

    st.dataframe(screener_df, use_container_width=True)

else:

    st.info("Belum ada hasil screening")

# ======================================
# LOAD ALL TRADES
# ======================================

try:

    trades = load_trades()

except Exception as e:

    st.error(f"Trade loading error: {e}")

    trades = []

# ======================================
# PORTFOLIO ANALYTICS
# ======================================

st.divider()

st.header("📊 Portfolio Analytics")

metrics = calculate_portfolio_metrics(trades)

# ======================================
# METRICS ROW 1
# ======================================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Trades", metrics["total_trades"])

col2.metric("Winrate", f"{metrics['winrate']}%")

col3.metric("Total PnL", f"Rp {metrics['total_pnl']:,.0f}")

col4.metric("Profit Factor", metrics["profit_factor"])

# ======================================
# METRICS ROW 2
# ======================================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Winning Trades", metrics["winning_trades"])

col2.metric("Losing Trades", metrics["losing_trades"])

col3.metric("Average RR", metrics["average_rr"])

col4.metric("Expectancy", metrics["expectancy"])

# ======================================
# BEST / WORST
# ======================================

col1, col2 = st.columns(2)

col1.success(f"🏆 Best Trade: " f"Rp {metrics['best_trade']:,.0f}")

col2.error(f"📉 Worst Trade: " f"Rp {metrics['worst_trade']:,.0f}")

# ======================================
# EQUITY CURVE
# ======================================

equity_df = generate_equity_curve(trades)

if not equity_df.empty:

    st.subheader("📈 Equity Curve")

    equity_fig = go.Figure()

    equity_fig.add_trace(
        go.Scatter(
            x=equity_df.index, y=equity_df["equity"], mode="lines", name="Equity"
        )
    )

    equity_fig.update_layout(height=400, xaxis_title="Trade", yaxis_title="Balance")

    st.plotly_chart(equity_fig, use_container_width=True)

# ======================================
# STRATEGY ANALYTICS
# ======================================

st.divider()

st.header("🧠 Strategy Analytics")

strategy_df = analyze_strategy_performance(trades)

if not strategy_df.empty:

    st.dataframe(strategy_df, use_container_width=True)

else:

    st.info("Belum ada strategy analytics")

# ======================================
# BACKTEST DASHBOARD
# ======================================

st.divider()

st.header("🧪 Strategy Backtest")

col1, col2 = st.columns(2)

backtest_symbol = col1.text_input("Backtest Symbol", value=symbol)

backtest_period = col2.selectbox("Backtest Period", ["6mo", "1y", "2y", "5y"])

# ======================================
# RUN BACKTEST
# ======================================

if st.button("🚀 Run Backtest"):

    with st.spinner("Running backtest..."):

        stats = run_backtest(backtest_symbol, period=backtest_period)

    if stats is None:

        st.error("Backtest gagal")

    else:

        st.success("Backtest selesai")

        # ======================================
        # METRICS
        # ======================================

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Return %", round(stats["Return [%]"], 2))

        col2.metric("Win Rate %", round(stats["Win Rate [%]"], 2))

        col3.metric("Max Drawdown %", round(stats["Max. Drawdown [%]"], 2))

        col4.metric("Total Trades", int(stats["# Trades"]))

        # ======================================
        # SECOND ROW
        # ======================================

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Sharpe Ratio", round(stats["Sharpe Ratio"], 2))

        col2.metric("Profit Factor", round(stats["Profit Factor"], 2))

        col3.metric("Expectancy", round(stats["Expectancy [%]"], 2))

        col4.metric("SQN", round(stats["SQN"], 2))

        # ======================================
        # EQUITY CURVE
        # ======================================

        st.subheader("📈 Backtest Equity Curve")

        equity_curve = stats["_equity_curve"]

        equity_fig = go.Figure()

        equity_fig.add_trace(
            go.Scatter(
                x=equity_curve.index,
                y=equity_curve["Equity"],
                mode="lines",
                name="Equity",
            )
        )

        equity_fig.update_layout(height=400, xaxis_title="Date", yaxis_title="Equity")

        st.plotly_chart(equity_fig, use_container_width=True)

        # ======================================
        # TRADE HISTORY
        # ======================================

        st.subheader("📋 Trade History")

        trades_df = stats["_trades"]

        st.dataframe(trades_df, use_container_width=True)

# ======================================
# PORTFOLIO CONSTRUCTION
# ======================================

st.divider()

st.header("🏗️ Portfolio Construction")

portfolio_data = analyze_portfolio(trades)

col1, col2, col3 = st.columns(3)

col1.metric("Open Positions", portfolio_data["total_positions"])

col2.metric("Total Exposure", f"Rp {portfolio_data['total_exposure']:,.0f}")

col3.metric("Risk Status", portfolio_data["risk_status"])

# ======================================
# SECTOR EXPOSURE
# ======================================

st.subheader("🏭 Sector Exposure")

sector_df = pd.DataFrame(
    {
        "Sector": list(portfolio_data["sector_exposure"].keys()),
        "Exposure": list(portfolio_data["sector_exposure"].values()),
    }
)

if not sector_df.empty:

    st.dataframe(sector_df, use_container_width=True)

# ======================================
# AI TRADE JOURNAL
# ======================================

st.divider()

st.header("📓 AI Trade Journal")

journal_data = load_journal()

if journal_data:

    journal_df = pd.DataFrame(journal_data)

    st.dataframe(journal_df, use_container_width=True)

else:

    st.info("Belum ada trade journal")

# ======================================
# PAPER TRADING HISTORY
# ======================================

st.divider()

st.header("📒 Paper Trading History")

if trades:

    trades_df = pd.DataFrame(trades)

    st.dataframe(trades_df, use_container_width=True)

else:

    st.info("Belum ada paper trade")

# ======================================
# AI LEARNING ENGINE
# ======================================

st.divider()

st.header("🧠 AI Learning Engine")

learning_df = analyze_learning_data(journal_data)

if not learning_df.empty:

    st.dataframe(learning_df, use_container_width=True)

else:

    st.info("Belum ada learning data")

# ======================================
# WALK FORWARD OPTIMIZATION
# ======================================

st.divider()

st.header("🧪 Walk Forward Optimization")

if history:

    optimization_data = optimize_parameters(screener_df)

    if optimization_data:

        col1, col2, col3 = st.columns(3)

        col1.metric("Optimal RSI", optimization_data["optimal_rsi"])

        col2.metric("Optimal ADX", optimization_data["optimal_adx"])

        col3.metric("Optimal Volatility", optimization_data["optimal_volatility"])

        st.info(optimization_data["insight"])

    else:

        st.info("Belum ada optimization data")

# ======================================
# AUTO PARAMETER ENGINE
# ======================================

st.divider()

st.header("🤖 Auto Parameter Engine")

current_parameters = load_parameters()

col1, col2, col3 = st.columns(3)

col1.metric("Min RSI", current_parameters["min_rsi"])

col2.metric("Min ADX", current_parameters["min_adx"])

col3.metric("Max Volatility", current_parameters["max_volatility"])

# ======================================
# AUTO TUNE BUTTON
# ======================================

if st.button("⚡ Auto Tune Parameters"):

    tuned = auto_tune_parameters(optimization_data)

    if tuned:

        st.success("AI parameters updated")

        st.json(tuned)

    else:

        st.warning("No optimization data")

# ======================================
# MARKET SIMULATOR ENGINE
# ======================================

st.divider()

st.header("🧪 Market Simulator")

if history:

    simulation_df = simulate_market_conditions(screener_df)

    if not simulation_df.empty:

        st.dataframe(simulation_df, use_container_width=True)

    else:

        st.info("Simulation unavailable")

# ======================================
# SYSTEM HEALTH
# ======================================

st.divider()

st.header("🩺 System Health")

health = validate_all_cache()

if health:

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Cache", health["total"])

    col2.metric("Valid", health["valid"])

    col3.metric("Invalid", health["invalid"])

    if health["invalid"] > 0:

        st.warning("Some cache files invalid")

    else:

        st.success("Cache healthy")

        # ======================================
# PERFORMANCE ANALYTICS
# ======================================

st.divider()

st.header("📊 Performance Analytics")

performance = analyze_performance(trades)

if performance:

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Winrate", f"{performance['winrate']}%")

    col2.metric("Profit Factor", performance["profit_factor"])

    col3.metric("Expectancy", performance["expectancy"])

    col4.metric("Sharpe Ratio", performance["sharpe_ratio"])

    col5, col6, col7 = st.columns(3)

    col5.metric("Avg Gain", performance["average_gain"])

    col6.metric("Avg Loss", performance["average_loss"])

    col7.metric("Max Drawdown", performance["max_drawdown"])

    # ======================================
# VALIDATION LAB
# ======================================

st.divider()

st.header("🧪 Validation Lab")

validation_df = validate_strategy_by_regime(trades)

if not validation_df.empty:

    st.dataframe(validation_df, use_container_width=True)

else:

    st.info("No validation data")

    # ======================================
# FORWARD TESTING
# ======================================

st.divider()

st.header("🚀 Forward Testing")

forward_signals = load_forward_signals()

forward_stats = analyze_forward_testing(forward_signals)

if forward_stats:

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Signals", forward_stats["total_signals"])

    col2.metric("Winrate", f"{forward_stats['winrate']}%")

    col3.metric("Avg Return", f"{forward_stats['average_return']}%")

    col4.metric("High Conf Return", f"{forward_stats['high_confidence_return']}%")

    forward_df = pd.DataFrame(forward_signals)

    st.dataframe(forward_df, use_container_width=True)

# ======================================
# SYSTEM STATUS
# ======================================

st.divider()

st.header("🩺 System Status")

log_file = Path("logs/system.log")

if log_file.exists():

    st.success("Logging System Active")

else:

    st.warning("Logging inactive")

backup_dir = Path("backups")

if backup_dir.exists():

    total_backup = len(list(backup_dir.glob("*")))

    st.info(f"Backups: {total_backup}")
