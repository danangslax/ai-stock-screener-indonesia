import shutil
import time

from datetime import datetime

from pathlib import Path

from infrastructure.logger import logger

from infrastructure.audit import audit_event

from infrastructure.recovery import safe_execute

# ======================================
# SOURCE DIRECTORY
# ======================================

DATA_DIR = Path("data")

# ======================================
# BACKUP DIRECTORY
# ======================================

BACKUP_DIR = Path("data") / "backups"

BACKUP_DIR.mkdir(parents=True, exist_ok=True)

# ======================================
# RETENTION POLICY
# ======================================

MAX_BACKUPS = 10

# ======================================
# GET DIRECTORY SIZE
# ======================================


def get_directory_size(path):

    total_size = 0

    for file in path.rglob("*"):

        if file.is_file():

            total_size += file.stat().st_size

    return round(total_size / (1024 * 1024), 2)


# ======================================
# CLEAN OLD BACKUPS
# ======================================


def cleanup_old_backups():

    try:

        backups = sorted(
            BACKUP_DIR.glob("backup_*"), key=lambda x: x.stat().st_mtime, reverse=True
        )

        if len(backups) <= MAX_BACKUPS:

            return

        old_backups = backups[MAX_BACKUPS:]

        for backup in old_backups:

            shutil.rmtree(backup)

            logger.info(f"Deleted old backup: " f"{backup.name}")

    except Exception as e:

        logger.error(f"Backup cleanup error: " f"{e}")


# ======================================
# VALIDATE BACKUP
# ======================================


def validate_backup(backup_path):

    try:

        if not backup_path.exists():

            return False

        required_dirs = ["cache", "snapshots", "logs"]

        for directory in required_dirs:

            if not (backup_path / directory).exists():

                logger.warning(f"Missing backup dir: " f"{directory}")

                return False

        return True

    except Exception as e:

        logger.error(f"Backup validation error: " f"{e}")

        return False


# ======================================
# BACKUP ENGINE
# ======================================


def main():

    try:

        start_time = time.time()

        logger.info("BACKUP SYSTEM STARTED")

        audit_event("BACKUP_START", "Disaster recovery backup")

        # ======================================
        # VALIDATE SOURCE
        # ======================================

        if not DATA_DIR.exists():

            logger.error("Data directory missing")

            return

        # ======================================
        # TIMESTAMP
        # ======================================

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # ======================================
        # TARGET DIRECTORY
        # ======================================

        target = BACKUP_DIR / f"backup_{timestamp}"

        logger.info(f"Creating backup: " f"{target.name}")

        # ======================================
        # CREATE BACKUP
        # ======================================

        result = safe_execute(shutil.copytree, DATA_DIR, target)

        if result is None:

            logger.error("Backup creation failed")

            return

        # ======================================
        # VALIDATE BACKUP
        # ======================================

        is_valid = validate_backup(target)

        if not is_valid:

            logger.error("Backup validation failed")

            return

        # ======================================
        # BACKUP SIZE
        # ======================================

        backup_size = get_directory_size(target)

        # ======================================
        # CLEANUP OLD BACKUPS
        # ======================================

        cleanup_old_backups()

        # ======================================
        # EXECUTION TIME
        # ======================================

        execution_time = round(time.time() - start_time, 2)

        # ======================================
        # FINAL SUMMARY
        # ======================================

        logger.info("=================================")

        logger.info("BACKUP COMPLETE")

        logger.info(f"Backup Name: " f"{target.name}")

        logger.info(f"Backup Size: " f"{backup_size} MB")

        logger.info(f"Execution Time: " f"{execution_time}s")

        logger.info("=================================")

        # ======================================
        # AUDIT
        # ======================================

        audit_event("BACKUP_COMPLETE", f"{target.name} | " f"{backup_size}MB")

    except Exception as e:

        logger.error(f"Backup System Error: " f"{e}")


# ======================================
# ENTRY POINT
# ======================================

if __name__ == "__main__":

    main()
