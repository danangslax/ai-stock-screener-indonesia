import traceback

from app.services.infrastructure.logger import logger

# ======================================
# SAFE EXECUTION
# ======================================


def safe_execute(func, *args, **kwargs):

    try:

        return func(*args, **kwargs)

    except Exception as e:

        logger.error(f"Crash Recovery: {e}")

        logger.error(traceback.format_exc())

        return None
