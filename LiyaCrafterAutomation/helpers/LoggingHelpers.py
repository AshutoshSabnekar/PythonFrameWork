"""
Test result logging and reporting helpers.
"""

import logging
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

__all__ = [
    "setup_test_logger",
    "log_comparison_result",
    "save_mismatch_report",
    "log_dataframe_summary",
]


def setup_test_logger(name: str = "test_framework", level: str = "INFO") -> logging.Logger:
    """Setup logger for tests with file and console handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    if logger.handlers:
        return logger

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )

    # File handler
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = Path(f"logs/test_run_{timestamp}.log")
    log_file.parent.mkdir(exist_ok=True)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def log_comparison_result(
        logger: logging.Logger,
        result: Dict[str, Any],
        test_name: str,
):
    """Log comparison result in structured format."""
    status = "PASS" if result.get("success") else "FAIL"
    logger.info(f"[{status}] {test_name}")

    if not result.get("success"):
        logger.error(f"  Message: {result.get('message', 'No message')}")
        meta = result.get("meta", {})
        if meta:
            logger.error(f"  Details: {meta}")


def save_mismatch_report(
        df: pd.DataFrame,
        filename: str,
        test_name: str,
        timestamp: Optional[str] = None,
):
    """Save mismatch DataFrame to CSV with metadata."""
    if df.empty:
        return

    timestamp = timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = Path(f"reports/mismatches/{test_name}_{timestamp}.csv")
    report_path.parent.mkdir(exist_ok=True)

    # Add metadata row
    meta_df = pd.DataFrame([{"test_name": test_name, "timestamp": timestamp, "row_count": len(df)}])
    combined = pd.concat([meta_df, df], ignore_index=True)
    combined.to_csv(report_path, index=False)

    return str(report_path)


def log_dataframe_summary(logger: logging.Logger, df: pd.DataFrame, name: str):
    """Log basic DataFrame stats."""
    logger.info(f"{name}: {len(df)} rows, {len(df.columns)} cols")
    logger.debug(f"Columns: {list(df.columns)}")
    logger.debug(f"Nulls: {df.isnull().sum().sum()}")
