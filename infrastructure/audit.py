from infrastructure.logger import logger

# ======================================
# AUDIT EVENT
# ======================================


def audit_event(action, detail=""):

    logger.info(f"[AUDIT] " f"Action={action} | " f"Detail={detail}")
