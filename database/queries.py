from database.db import supabase

# ======================================
# SAVE SCREENER RESULTS
# ======================================

def save_screener_results(df):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if supabase is None:

            print(
                "❌ Supabase not connected"
            )

            return

        if df.empty:

            print(
                "⚠️ Empty screener result"
            )

            return

        # ======================================
        # CONVERT DATAFRAME
        # ======================================

        records = df.to_dict(
            orient="records"
        )

        # ======================================
        # INSERT DATABASE
        # ======================================

        response = supabase.table(
            "screener_results"
        ).insert(records).execute()

        print(
            "✅ Screener results saved"
        )

        return response

    except Exception as e:

        print(
            f"❌ Database Error: {e}"
        )

        return None


# ======================================
# LOAD SCREENER HISTORY
# ======================================

def load_screener_history(limit=50):

    try:

        # ======================================
        # VALIDATION
        # ======================================

        if supabase is None:

            print(
                "❌ Supabase not connected"
            )

            return []

        # ======================================
        # LOAD DATA
        # ======================================

        response = supabase.table(
            "screener_results"
        ).select("*").order(
            "created_at",
            desc=True
        ).limit(limit).execute()

        # ======================================
        # EMPTY RESPONSE
        # ======================================

        if not response.data:

            return []

        return response.data

    except Exception as e:

        print(
            f"❌ Load History Error: {e}"
        )

        return []


# ======================================
# DELETE OLD HISTORY
# OPTIONAL MAINTENANCE
# ======================================

def delete_old_history(days=30):

    try:

        if supabase is None:

            return

        response = supabase.rpc(
            "delete_old_screener_results",
            {
                "days_old": days
            }
        ).execute()

        print(
            "🗑️ Old screener history deleted"
        )

        return response

    except Exception as e:

        print(
            f"❌ Delete History Error: {e}"
        )

        return None