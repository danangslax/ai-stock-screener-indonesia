import plotly.graph_objects as go
import pandas as pd

# ======================================
# EQUITY CURVE CHART
# ======================================


def create_equity_curve_chart(
    equity_df,
    title="Equity Curve",
):

    try:

        if equity_df.empty:

            return None

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=equity_df.index,
                y=equity_df["equity"],
                mode="lines",
                name="Equity",
            )
        )

        fig.update_layout(
            height=500,
            template="plotly_dark",
            title=title,
            xaxis_title="Trade",
            yaxis_title="Equity",
        )

        return fig

    except Exception as e:

        print(f"❌ Equity chart error: {e}")

        return None


# ======================================
# PNL DISTRIBUTION CHART
# ======================================


def create_pnl_distribution_chart(
    trades_df,
    title="PnL Distribution",
):

    try:

        if trades_df.empty:

            return None

        if "profit_loss" not in trades_df.columns:

            return None

        fig = go.Figure()

        fig.add_trace(
            go.Histogram(
                x=trades_df["profit_loss"],
                nbinsx=30,
                name="PnL",
            )
        )

        fig.update_layout(
            height=450,
            template="plotly_dark",
            title=title,
            xaxis_title="Profit Loss",
            yaxis_title="Frequency",
        )

        return fig

    except Exception as e:

        print(f"❌ PnL chart error: {e}")

        return None


# ======================================
# WIN LOSS PIE CHART
# ======================================


def create_win_loss_chart(
    wins,
    losses,
    title="Win Loss Ratio",
):

    try:

        fig = go.Figure()

        fig.add_trace(
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

        fig.update_layout(
            height=450,
            template="plotly_dark",
            title=title,
        )

        return fig

    except Exception as e:

        print(f"❌ Win loss chart error: {e}")

        return None


# ======================================
# STRATEGY PERFORMANCE CHART
# ======================================


def create_strategy_chart(
    strategy_df,
    title="Strategy Performance",
):

    try:

        if strategy_df.empty:

            return None

        required_columns = [
            "strategy",
            "Total_PnL",
        ]

        for col in required_columns:

            if col not in strategy_df.columns:

                return None

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=strategy_df["strategy"],
                y=strategy_df["Total_PnL"],
                name="PnL",
            )
        )

        fig.update_layout(
            height=450,
            template="plotly_dark",
            title=title,
            xaxis_title="Strategy",
            yaxis_title="Total PnL",
        )

        return fig

    except Exception as e:

        print(f"❌ Strategy chart error: {e}")

        return None


# ======================================
# MONTHLY PERFORMANCE CHART
# ======================================


def create_monthly_performance_chart(
    monthly_df,
    title="Monthly Performance",
):

    try:

        if monthly_df.empty:

            return None

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=monthly_df["month"],
                y=monthly_df["profit_loss"],
                name="Monthly PnL",
            )
        )

        fig.update_layout(
            height=450,
            template="plotly_dark",
            title=title,
            xaxis_title="Month",
            yaxis_title="Profit Loss",
        )

        return fig

    except Exception as e:

        print(f"❌ Monthly chart error: {e}")

        return None


# ======================================
# CONFIDENCE SCATTER CHART
# ======================================


def create_confidence_chart(
    df,
    x_col="confidence",
    y_col="forward_return",
    label_col="symbol",
    title="Confidence Analysis",
):

    try:

        if df.empty:

            return None

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df[x_col],
                y=df[y_col],
                mode="markers+text",
                text=df[label_col],
                textposition="top center",
                name="Signals",
            )
        )

        fig.update_layout(
            height=500,
            template="plotly_dark",
            title=title,
            xaxis_title=x_col,
            yaxis_title=y_col,
        )

        return fig

    except Exception as e:

        print(f"❌ Confidence chart error: {e}")

        return None


# ======================================
# MARKET REGIME CHART
# ======================================


def create_market_regime_chart(
    df,
    regime_col="Market_Regime",
    score_col="Simulation_Score",
    title="Market Regime Analysis",
):

    try:

        if df.empty:

            return None

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=df[regime_col],
                y=df[score_col],
                name="Score",
            )
        )

        fig.update_layout(
            height=450,
            template="plotly_dark",
            title=title,
            xaxis_title="Market Regime",
            yaxis_title="Score",
        )

        return fig

    except Exception as e:

        print(f"❌ Regime chart error: {e}")

        return None


# ======================================
# SECTOR STRENGTH CHART
# ======================================


def create_sector_strength_chart(
    sector_df,
    title="Sector Strength",
):

    try:

        if sector_df.empty:

            return None

        required_columns = [
            "Sector",
            "Score",
        ]

        for col in required_columns:

            if col not in sector_df.columns:

                return None

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=sector_df["Sector"],
                y=sector_df["Score"],
                name="Sector Score",
            )
        )

        fig.update_layout(
            height=500,
            template="plotly_dark",
            title=title,
            xaxis_title="Sector",
            yaxis_title="Score",
        )

        return fig

    except Exception as e:

        print(f"❌ Sector chart error: {e}")

        return None


# ======================================
# PORTFOLIO EXPOSURE CHART
# ======================================


def create_portfolio_exposure_chart(
    sector_exposure,
    title="Portfolio Exposure",
):

    try:

        if not sector_exposure:

            return None

        labels = list(sector_exposure.keys())

        values = list(sector_exposure.values())

        fig = go.Figure()

        fig.add_trace(
            go.Pie(
                labels=labels,
                values=values,
                hole=0.4,
            )
        )

        fig.update_layout(
            height=450,
            template="plotly_dark",
            title=title,
        )

        return fig

    except Exception as e:

        print(f"❌ Portfolio chart error: {e}")

        return None


# ======================================
# GENERIC BAR CHART
# ======================================


def create_bar_chart(
    df,
    x_col,
    y_col,
    title="Bar Chart",
):

    try:

        if df.empty:

            return None

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=df[x_col],
                y=df[y_col],
                name=y_col,
            )
        )

        fig.update_layout(
            height=450,
            template="plotly_dark",
            title=title,
            xaxis_title=x_col,
            yaxis_title=y_col,
        )

        return fig

    except Exception as e:

        print(f"❌ Bar chart error: {e}")

        return None


# ======================================
# GENERIC LINE CHART
# ======================================


def create_line_chart(
    df,
    x_col,
    y_col,
    title="Line Chart",
):

    try:

        if df.empty:

            return None

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df[x_col],
                y=df[y_col],
                mode="lines",
                name=y_col,
            )
        )

        fig.update_layout(
            height=450,
            template="plotly_dark",
            title=title,
            xaxis_title=x_col,
            yaxis_title=y_col,
        )

        return fig

    except Exception as e:

        print(f"❌ Line chart error: {e}")

        return None
