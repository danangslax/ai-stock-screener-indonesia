import os

from dotenv import load_dotenv
from supabase import create_client

# ======================================
# LOAD ENVIRONMENT VARIABLES
# ======================================

load_dotenv()

SUPABASE_URL = os.getenv(
    "SUPABASE_URL"
)

SUPABASE_KEY = os.getenv(
    "SUPABASE_KEY"
)

# ======================================
# VALIDATION
# ======================================

if not SUPABASE_URL:

    raise ValueError(
        "SUPABASE_URL is missing"
    )

if not SUPABASE_KEY:

    raise ValueError(
        "SUPABASE_KEY is missing"
    )

# ======================================
# CREATE SUPABASE CLIENT
# ======================================

try:

    supabase = create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )

    print(
        "✅ Supabase connected"
    )

except Exception as e:

    print(
        f"❌ Supabase Error: {e}"
    )

    supabase = None