import shutil

from datetime import datetime

from pathlib import Path

# ======================================
# SOURCE
# ======================================

DATA_DIR = Path("data")

# ======================================
# BACKUP DIR
# ======================================

BACKUP_DIR = Path("backups")

BACKUP_DIR.mkdir(parents=True, exist_ok=True)

# ======================================
# BACKUP ENGINE
# ======================================


def main():

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    target = BACKUP_DIR / f"backup_{timestamp}"

    shutil.copytree(DATA_DIR, target)

    print(f"✅ Backup saved: " f"{target}")


# ======================================
# ENTRY POINT
# ======================================

if __name__ == "__main__":

    main()
