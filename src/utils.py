# ---------------------------------------
# utils.py for notebook work
# ---------------------------------------
from datetime import datetime
import time


def current_timestamp():
    """
    Returns the current timestamp.
    """
    return datetime.now()


def current_time():
    """
    Returns the current time in seconds.
    """
    return time.time()


def calculate_elapsed_time(start_time):
    """
    Calculates elapsed time in seconds.
    """
    return round(time.time() - start_time, 2)

# ---------------------------------------
# Updated utils.py
# ---------------------------------------

"""
Utility functions used across the project.
"""

from datetime import datetime
from pathlib import Path
import time

import pandas as pd

# ============================================================
# Prompt Utilities
# ============================================================

def load_prompt(prompt_path: Path) -> str:
    """
    Loads a prompt from a text file.

    Args:
        prompt_path (Path): Prompt file path.

    Returns:
        str
    """
    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read()


# ============================================================
# File Discovery
# ============================================================

def discover_files(input_dir: Path, pattern: str = "*.*") -> pd.DataFrame:
    """
    Discovers files inside a directory and returns
    a standardized DataFrame.

    Args:
        input_dir (Path)
        pattern (str)

    Returns:
        pd.DataFrame
    """

    files = sorted(input_dir.glob(pattern))

    if not files:
        raise FileNotFoundError(
            f"No files found in: {input_dir}"
        )

    return pd.DataFrame(
        {
            "file_name": [file.name for file in files],
            "file_path": [str(file) for file in files],
            "file_size_kb": [
                round(file.stat().st_size / 1024, 2)
                for file in files
            ],
            "status": "Pending",
        }
    )


# ============================================================
# Output Utilities
# ============================================================

def save_dataframe(
    dataframe: pd.DataFrame,
    output_path: Path,
):
    """
    Saves a DataFrame to CSV.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe.to_csv(
        output_path,
        index=False,
    )


# ============================================================
# Summary Utility
# ============================================================

def print_section(title: str):
    """
    Prints a formatted section title.
    """

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)