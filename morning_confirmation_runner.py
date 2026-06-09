from core.confirmation import (
    morning_confirmation
)

from database.queries import (
    load_screener_history
)

from core.notifier import (
    send_telegram_message
)

# ======================================
# LOAD HISTORY
# ======================================

history = load_screener_history(limit=10)

if not history:

    print("No screener history found")

    exit()

# ======================================
# MORNING CHECK
# ======================================

for stock in history:

    symbol = stock["Symbol"]

    confirmation = morning_confirmation(
        symbol
    )

    message = f"""
☀️ MORNING CONFIRMATION

{symbol}

Status: {confirmation}
"""

    print(message)

    send_telegram_message(message)

print("Morning confirmation done.")
