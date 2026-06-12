from core.cache_validator import validate_all_cache

from runners.download_market_data import download_stock

# ======================================
# REPAIR CACHE ENGINE
# ======================================


def main():

    print("🛠️ Cache Repair Engine")

    summary = validate_all_cache()

    invalid_files = summary.get("invalid_files", [])

    if not invalid_files:

        print("✅ Cache healthy")

        return

    print(f"⚠️ Invalid files: " f"{len(invalid_files)}")

    # ======================================
    # REPAIR LOOP
    # ======================================

    for file_name in invalid_files:

        symbol = file_name.replace(".parquet", "")

        print(f"🔧 Repairing " f"{symbol}")

        download_stock(symbol)

    print("✅ Repair complete")


# ======================================
# ENTRY POINT
# ======================================

if __name__ == "__main__":

    main()
