import os
import json
import time
import psutil
import pandas as pd

from pathlib import Path
from datetime import datetime

# ======================================
# SAFE DATAFRAME
# ======================================


def safe_dataframe(data):

    try:

        if data is None:

            return pd.DataFrame()

        if isinstance(
            data,
            pd.DataFrame,
        ):

            return data

        if isinstance(
            data,
            list,
        ):

            return pd.DataFrame(data)

        if isinstance(
            data,
            dict,
        ):

            return pd.DataFrame([data])

        return pd.DataFrame()

    except Exception as e:

        print(f"❌ Safe dataframe error: {e}")

        return pd.DataFrame()


# ======================================
# SAFE FLOAT
# ======================================


def safe_float(
    value,
    default=0,
):

    try:

        return float(value)

    except Exception:

        return default


# ======================================
# SAFE INTEGER
# ======================================


def safe_int(
    value,
    default=0,
):

    try:

        return int(value)

    except Exception:

        return default


# ======================================
# SAFE STRING
# ======================================


def safe_string(
    value,
    default="",
):

    try:

        if value is None:

            return default

        return str(value)

    except Exception:

        return default


# ======================================
# LOAD JSON FILE
# ======================================


def load_json_file(
    file_path,
):

    try:

        path = Path(file_path)

        if not path.exists():

            return {}

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(f)

    except Exception as e:

        print(f"❌ Load JSON error: {e}")

        return {}


# ======================================
# SAVE JSON FILE
# ======================================


def save_json_file(
    file_path,
    data,
):

    try:

        path = Path(file_path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                default=str,
            )

        return True

    except Exception as e:

        print(f"❌ Save JSON error: {e}")

        return False


# ======================================
# GET FILE SIZE
# ======================================


def get_file_size(
    file_path,
):

    try:

        path = Path(file_path)

        if not path.exists():

            return 0

        return path.stat().st_size

    except Exception as e:

        print(f"❌ File size error: {e}")

        return 0


# ======================================
# FORMAT FILE SIZE
# ======================================


def format_file_size(
    size_bytes,
):

    try:

        if size_bytes >= 1024**3:

            return f"{size_bytes / (1024**3):.2f} GB"

        if size_bytes >= 1024**2:

            return f"{size_bytes / (1024**2):.2f} MB"

        if size_bytes >= 1024:

            return f"{size_bytes / 1024:.2f} KB"

        return f"{size_bytes} B"

    except Exception as e:

        print(f"❌ Format size error: {e}")

        return "0 B"


# ======================================
# DIRECTORY FILE COUNT
# ======================================


def count_files(
    directory,
    extension=None,
):

    try:

        path = Path(directory)

        if not path.exists():

            return 0

        if extension:

            return len(list(path.glob(f"*.{extension}")))

        return len([file for file in path.iterdir() if file.is_file()])

    except Exception as e:

        print(f"❌ Count files error: {e}")

        return 0


# ======================================
# GET SYSTEM HEALTH
# ======================================


def get_system_health():

    try:

        cpu_usage = psutil.cpu_percent()

        memory_usage = psutil.virtual_memory().percent

        disk_usage = psutil.disk_usage("/").percent

        return {
            "cpu_usage": round(
                cpu_usage,
                2,
            ),
            "memory_usage": round(
                memory_usage,
                2,
            ),
            "disk_usage": round(
                disk_usage,
                2,
            ),
        }

    except Exception as e:

        print(f"❌ System health error: {e}")

        return {
            "cpu_usage": 0,
            "memory_usage": 0,
            "disk_usage": 0,
        }


# ======================================
# CHECK REQUIRED COLUMNS
# ======================================


def validate_columns(
    df,
    required_columns,
):

    try:

        if df.empty:

            return False

        missing = [col for col in required_columns if col not in df.columns]

        return len(missing) == 0

    except Exception as e:

        print(f"❌ Validate column error: {e}")

        return False


# ======================================
# GET CURRENT TIME
# ======================================


def get_current_time():

    try:

        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    except Exception as e:

        print(f"❌ Current time error: {e}")

        return "-"


# ======================================
# GET CURRENT DATE
# ======================================


def get_current_date():

    try:

        return datetime.now().strftime("%Y-%m-%d")

    except Exception as e:

        print(f"❌ Current date error: {e}")

        return "-"


# ======================================
# EXECUTION TIMER
# ======================================


def execution_timer():

    return time.time()


# ======================================
# CALCULATE EXECUTION TIME
# ======================================


def calculate_execution_time(
    start_time,
):

    try:

        end_time = time.time()

        return round(
            end_time - start_time,
            2,
        )

    except Exception as e:

        print(f"❌ Execution timer error: {e}")

        return 0


# ======================================
# CREATE DIRECTORY
# ======================================


def ensure_directory(
    directory,
):

    try:

        Path(directory).mkdir(
            parents=True,
            exist_ok=True,
        )

        return True

    except Exception as e:

        print(f"❌ Create directory error: {e}")

        return False


# ======================================
# CHECK FILE EXISTS
# ======================================


def file_exists(
    file_path,
):

    try:

        return Path(file_path).exists()

    except Exception as e:

        print(f"❌ File exists error: {e}")

        return False


# ======================================
# REMOVE FILE
# ======================================


def remove_file(
    file_path,
):

    try:

        path = Path(file_path)

        if path.exists():

            path.unlink()

        return True

    except Exception as e:

        print(f"❌ Remove file error: {e}")

        return False


# ======================================
# GET CACHE FILES
# ======================================


def get_cache_files():

    try:

        cache_dir = Path("data") / "cache"

        if not cache_dir.exists():

            return []

        return list(cache_dir.glob("*.parquet"))

    except Exception as e:

        print(f"❌ Cache file error: {e}")

        return []


# ======================================
# CACHE SUMMARY
# ======================================


def get_cache_summary():

    try:

        files = get_cache_files()

        total_size = 0

        for file in files:

            total_size += file.stat().st_size

        return {
            "total_files": len(files),
            "total_size": format_file_size(total_size),
        }

    except Exception as e:

        print(f"❌ Cache summary error: {e}")

        return {
            "total_files": 0,
            "total_size": "0 B",
        }


# ======================================
# CLEAN DATAFRAME NAN
# ======================================


def clean_dataframe(
    df,
):

    try:

        if df.empty:

            return df

        df = df.copy()

        df = df.dropna(how="all")

        df = df.fillna(0)

        return df

    except Exception as e:

        print(f"❌ Clean dataframe error: {e}")

        return pd.DataFrame()


# ======================================
# SORT DATAFRAME
# ======================================


def sort_dataframe(
    df,
    column,
    ascending=False,
):

    try:

        if df.empty:

            return df

        if column not in df.columns:

            return df

        return df.sort_values(
            by=column,
            ascending=ascending,
        ).reset_index(drop=True)

    except Exception as e:

        print(f"❌ Sort dataframe error: {e}")

        return df


# ======================================
# LIMIT DATAFRAME
# ======================================


def limit_dataframe(
    df,
    limit=10,
):

    try:

        if df.empty:

            return df

        return df.head(limit)

    except Exception as e:

        print(f"❌ Limit dataframe error: {e}")

        return df


# ======================================
# GET ENV VARIABLE
# ======================================


def get_env_variable(
    key,
    default=None,
):

    try:

        return os.getenv(
            key,
            default,
        )

    except Exception as e:

        print(f"❌ Env variable error: {e}")

        return default
