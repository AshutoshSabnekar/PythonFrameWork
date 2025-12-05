"""
Data processing and validation helper functions for semantic views.
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Union
from datetime import datetime

__all__ = [
    "normalize_column_names",
    "safe_to_datetime",
    "safe_to_numeric",
    "assert_non_empty",
    "compare_floats",
    "remove_duplicates",
    "standardize_nulls",
    "get_column_stats",
]


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Convert column names to snake_case, trim spaces, remove special chars."""
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9_]", "_", regex=True)
        .str.replace(r"_+", "_", regex=True)
        .str.strip("_")
    )
    return df


def safe_to_datetime(series: pd.Series, fmt: Optional[str] = None) -> pd.Series:
    """Convert to datetime safely, preserving nulls."""
    if fmt:
        return pd.to_datetime(series, format=fmt, errors="coerce")
    return pd.to_datetime(series, errors="coerce")


def safe_to_numeric(series: pd.Series, precision: int = 2) -> pd.Series:
    """Convert to numeric safely, rounding to specified precision."""
    numeric_series = pd.to_numeric(series, errors="coerce")
    return numeric_series.round(precision)


def assert_non_empty(df: pd.DataFrame, name: str = "DataFrame") -> None:
    """Raise ValueError if DataFrame is empty."""
    if df.empty:
        raise ValueError(f"{name} is empty")
    if df.isnull().all().all():
        raise ValueError(f"{name} contains only null values")


def compare_floats(val1: float, val2: float, tolerance: float = 1e-6) -> bool:
    """Compare floats with configurable tolerance."""
    return abs(val1 - val2) <= tolerance


def remove_duplicates(df: pd.DataFrame, subset: Optional[List[str]] = None) -> pd.DataFrame:
    """Remove duplicates, keeping first occurrence."""
    return df.drop_duplicates(subset=subset, keep="first").reset_index(drop=True)


def standardize_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Convert common null representations to NaN."""
    for col in df.columns:
        mask = df[col].astype(str).isin(["", "null", "NULL", "None", "NA", "NaN"])
        df.loc[mask, col] = np.nan
    return df


def get_column_stats(df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """Get basic stats for numeric columns."""
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()

    stats = []
    for col in columns:
        if col in df.columns:
            stats.append({
                "column": col,
                "count": df[col].count(),
                "null_count": df[col].isnull().sum(),
                "mean": df[col].mean(),
                "min": df[col].min(),
                "max": df[col].max(),
            })
    return pd.DataFrame(stats)
