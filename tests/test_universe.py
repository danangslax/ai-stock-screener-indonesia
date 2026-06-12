from core.universe_filter import filter_universe

from screener.screener import IDX_STOCKS

# ======================================
# RUN FILTER
# ======================================

filtered = filter_universe(IDX_STOCKS)

# ======================================
# RESULT
# ======================================

print("")

print("FINAL RESULT")

print(f"Total: {len(filtered)}")

print("")

for symbol in filtered[:20]:

    print(symbol)
