import traceback

from infrastructure.logger import logger

# ======================================
# SAFE EXECUTION
# ======================================


def safe_execute(func, *args, default=None, **kwargs):

    try:

        return func(*args, **kwargs)

    except Exception as e:

        logger.error(f"[RECOVERY] " f"Function: " f"{func.__name__} | " f"Error: {e}")

        logger.error(traceback.format_exc())

        return default
