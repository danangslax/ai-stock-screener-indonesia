from datetime import datetime

from app.services.infrastructure.logger import logger

# ======================================
# AUDIT EVENT
# ======================================


def audit_event(action, detail=""):

    timestamp = str(datetime.now())

    logger.info(f"[AUDIT] " f"{timestamp} | " f"{action} | " f"{detail}")
