import time

from pathlib import Path

from infrastructure.logger import logger

from infrastructure.audit import audit_event

from infrastructure.recovery import safe_execute

from infrastructure.cache_validator import validate_all_cache, validate_cache_file

from app.runners.download_market_data import download_stock

# ======================================
# CACHE DIRECTORY
# ======================================

CACHE_DIR = Path("data") / "cache"

# ======================================
# REPAIR CACHE ENGINE
# ======================================


def main():

    try:

        start_time = time.time()

        logger.info("CACHE REPAIR STARTED")

        audit_event("CACHE_REPAIR_START", "Self-healing cache engine")

        # ======================================
        # VALIDATE CACHE
        # ======================================

        summary = safe_execute(validate_all_cache)

        if not summary:

            logger.error("Cache validation failed")

            return

        invalid_files = summary.get("invalid_files", [])

        total_files = summary.get("total", 0)

        valid_files = summary.get("valid", 0)

        invalid_count = len(invalid_files)

        logger.info(f"Total Cache Files: " f"{total_files}")

        logger.info(f"Valid Files: " f"{valid_files}")

        logger.info(f"Invalid Files: " f"{invalid_count}")

        # ======================================
        # HEALTH STATUS
        # ======================================

        health_status = "HEALTHY"

        if invalid_count > 0:

            health_status = "WARNING"

        if invalid_count > 10:

            health_status = "CRITICAL"

        logger.info(f"Health Status: " f"{health_status}")

        # ======================================
        # HEALTHY CACHE
        # ======================================

        if not invalid_files:

            logger.info("Cache fully healthy")

            audit_event("CACHE_HEALTHY", "No repair needed")

            return

        # ======================================
        # REPAIR LOOP
        # ======================================

        repaired = 0

        failed = 0

        for file_name in invalid_files:

            try:

                symbol = file_name.replace(".parquet", "")

                logger.info(f"Repairing {symbol}")

                file_path = CACHE_DIR / file_name

                # ======================================
                # REMOVE CORRUPTED FILE
                # ======================================

                if file_path.exists():

                    try:

                        file_path.unlink()

                        logger.info(f"Deleted corrupted cache: " f"{symbol}")

                    except Exception as delete_error:

                        logger.warning(
                            f"Delete failed " f"{symbol}: " f"{delete_error}"
                        )

                # ======================================
                # DOWNLOAD REPAIR
                # ======================================

                result = safe_execute(download_stock, symbol)

                # ======================================
                # REVALIDATE
                # ======================================

                if result:

                    validation = validate_cache_file(CACHE_DIR / f"{symbol}.parquet")

                    if validation:

                        repaired += 1

                        logger.info(f"Repair success: " f"{symbol}")

                    else:

                        failed += 1

                        logger.warning(f"Repair validation failed: " f"{symbol}")

                else:

                    failed += 1

                    logger.warning(f"Repair failed: " f"{symbol}")

            except Exception as repair_error:

                failed += 1

                logger.error(f"Repair Error " f"{file_name}: " f"{repair_error}")

        # ======================================
        # EXECUTION TIME
        # ======================================

        execution_time = round(time.time() - start_time, 2)

        # ======================================
        # FINAL HEALTH SCORE
        # ======================================

        repair_success_rate = 0

        if invalid_count > 0:

            repair_success_rate = round((repaired / invalid_count) * 100, 2)

        final_health = "HEALTHY"

        if repair_success_rate < 80:

            final_health = "WARNING"

        if repair_success_rate < 50:

            final_health = "CRITICAL"

        # ======================================
        # FINAL SUMMARY
        # ======================================

        logger.info("=================================")

        logger.info("CACHE REPAIR COMPLETE")

        logger.info(f"Repaired: " f"{repaired}")

        logger.info(f"Failed: " f"{failed}")

        logger.info(f"Repair Success Rate: " f"{repair_success_rate}%")

        logger.info(f"Final Health: " f"{final_health}")

        logger.info(f"Execution Time: " f"{execution_time}s")

        logger.info("=================================")

        # ======================================
        # AUDIT EVENT
        # ======================================

        audit_event(
            "CACHE_REPAIR_COMPLETE",
            f"Repaired={repaired} | " f"Failed={failed} | " f"Health={final_health}",
        )

    except Exception as e:

        logger.error(f"Cache Repair Error: {e}")


# ======================================
# ENTRY POINT
# ======================================

if __name__ == "__main__":

    main()
