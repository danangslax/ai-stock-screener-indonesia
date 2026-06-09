from database.db import supabase

# ======================================
# SAVE SCREENER RESULTS
# ======================================

def save_screener_results(df):

    try:

        if df.empty:
            return

        records = df.to_dict(
            orient="records"
        )

        response = supabase.table(
            "screener_results"
        ).insert(records).execute()

        return response

    except Exception as e:

        print("Database Error:", e)


# ======================================
# LOAD HISTORY
# ======================================

def load_screener_history(limit=50):

    response = supabase.table(
        "screener_results"
    ).select("*").order(
        "created_at",
        desc=True
    ).limit(limit).execute()

    return response.data