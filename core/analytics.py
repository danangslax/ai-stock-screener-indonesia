import pandas as pd

# ======================================
# PORTFOLIO ANALYTICS
# ======================================

def calculate_portfolio_metrics(
    trades
):

    # ======================================
    # EMPTY VALIDATION
    # ======================================

    if not trades:

        return {

            "total_trades": 0,

            "open_trades": 0,

            "closed_trades": 0,

            "winning_trades": 0,

            "losing_trades": 0,

            "winrate": 0,

            "total_pnl": 0,

            "average_pnl": 0,

            "best_trade": 0,

            "worst_trade": 0,

            "average_rr": 0,

            "profit_factor": 0,

            "expectancy": 0
        }

    # ======================================
    # DATAFRAME
    # ======================================

    df = pd.DataFrame(trades)

    # ======================================
    # TOTAL TRADES
    # ======================================

    total_trades = len(df)

    open_trades = len(
        df[
            df["status"] == "OPEN"
        ]
    )

    closed_df = df[
        df["status"] == "CLOSED"
    ]

    closed_trades = len(closed_df)

    # ======================================
    # NO CLOSED TRADES
    # ======================================

    if closed_df.empty:

        return {

            "total_trades": total_trades,

            "open_trades": open_trades,

            "closed_trades": 0,

            "winning_trades": 0,

            "losing_trades": 0,

            "winrate": 0,

            "total_pnl": 0,

            "average_pnl": 0,

            "best_trade": 0,

            "worst_trade": 0,

            "average_rr": 0,

            "profit_factor": 0,

            "expectancy": 0
        }

    # ======================================
    # PNL
    # ======================================

    closed_df["profit_loss"] = pd.to_numeric(

        closed_df["profit_loss"],

        errors="coerce"
    ).fillna(0)

    total_pnl = round(

        closed_df["profit_loss"].sum(),

        2
    )

    average_pnl = round(

        closed_df["profit_loss"].mean(),

        2
    )

    best_trade = round(

        closed_df["profit_loss"].max(),

        2
    )

    worst_trade = round(

        closed_df["profit_loss"].min(),

        2
    )

    # ======================================
    # WIN / LOSS
    # ======================================

    winning_trades = len(

        closed_df[
            closed_df["profit_loss"] > 0
        ]
    )

    losing_trades = len(

        closed_df[
            closed_df["profit_loss"] <= 0
        ]
    )

    # ======================================
    # WINRATE
    # ======================================

    winrate = round(

        (
            winning_trades
            /
            closed_trades
        ) * 100,

        2
    )

    # ======================================
    # PROFIT FACTOR
    # ======================================

    gross_profit = closed_df[
        closed_df["profit_loss"] > 0
    ]["profit_loss"].sum()

    gross_loss = abs(

        closed_df[
            closed_df["profit_loss"] < 0
        ]["profit_loss"].sum()
    )

    if gross_loss > 0:

        profit_factor = round(

            gross_profit
            /
            gross_loss,

            2
        )

    else:

        profit_factor = 0

    # ======================================
    # EXPECTANCY
    # ======================================

    expectancy = round(

        total_pnl
        /
        closed_trades,

        2
    )

    # ======================================
    # RISK REWARD
    # ======================================

    if (
        "risk_reward"
        in closed_df.columns
    ):

        average_rr = round(

            pd.to_numeric(

                closed_df[
                    "risk_reward"
                ],

                errors="coerce"
            ).mean(),

            2
        )

    else:

        average_rr = 0

    # ======================================
    # RETURN RESULT
    # ======================================

    return {

        "total_trades": total_trades,

        "open_trades": open_trades,

        "closed_trades": closed_trades,

        "winning_trades": winning_trades,

        "losing_trades": losing_trades,

        "winrate": winrate,

        "total_pnl": total_pnl,

        "average_pnl": average_pnl,

        "best_trade": best_trade,

        "worst_trade": worst_trade,

        "average_rr": average_rr,

        "profit_factor": profit_factor,

        "expectancy": expectancy
    }

# ======================================
# EQUITY CURVE
# ======================================

def generate_equity_curve(
    trades,
    starting_balance=100_000_000
):

    if not trades:

        return pd.DataFrame()

    df = pd.DataFrame(trades)

    closed_df = df[
        df["status"] == "CLOSED"
    ].copy()

    if closed_df.empty:

        return pd.DataFrame()

    # ======================================
    # SORT DATE
    # ======================================

    if "created_at" in closed_df.columns:

        closed_df = closed_df.sort_values(
            by="created_at"
        )

    # ======================================
    # PNL
    # ======================================

    closed_df["profit_loss"] = pd.to_numeric(

        closed_df["profit_loss"],

        errors="coerce"
    ).fillna(0)

    # ======================================
    # EQUITY
    # ======================================

    equity = []

    current_balance = (
        starting_balance
    )

    for pnl in closed_df[
        "profit_loss"
    ]:

        current_balance += pnl

        equity.append(
            current_balance
        )

    closed_df["equity"] = equity

    return closed_df