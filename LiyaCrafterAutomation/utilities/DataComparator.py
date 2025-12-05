from typing import List, Dict, Any, Optional, Tuple
import pandas as pd


class DataComparisonResult:
    """
    Simple result object for comparisons.
    """
    def __init__(
        self,
        success: bool,
        message: str,
        details: Optional[pd.DataFrame] = None,
        meta: Optional[Dict[str, Any]] = None,
    ):
        self.success = success
        self.message = message
        self.details = details
        self.meta = meta or {}


class DataComparator:
    """
    Utility class to compare two pandas DataFrames for semantic view validations.
    Supports:
    - Row count comparison
    - Schema/column comparison
    - Key-based row-level comparison using outer join + indicator
    """

    def compare_row_count(
        self,
        actual: pd.DataFrame,
        expected: pd.DataFrame,
        tolerance: int = 0,
    ) -> DataComparisonResult:
        """
        Compare row counts with an allowed difference (tolerance).
        """
        actual_count = len(actual)
        expected_count = len(expected)
        diff = abs(actual_count - expected_count)

        if diff <= tolerance:
            return DataComparisonResult(
                success=True,
                message=f"Row count matches within tolerance. "
                        f"Actual={actual_count}, Expected={expected_count}, Tolerance={tolerance}",
                meta={
                    "actual_count": actual_count,
                    "expected_count": expected_count,
                    "tolerance": tolerance,
                },
            )

        return DataComparisonResult(
            success=False,
            message=f"Row count mismatch. Actual={actual_count}, Expected={expected_count}, "
                    f"Difference={diff}, Tolerance={tolerance}",
            meta={
                "actual_count": actual_count,
                "expected_count": expected_count,
                "difference": diff,
                "tolerance": tolerance,
            },
        )

    def compare_schema(
        self,
        actual: pd.DataFrame,
        expected: pd.DataFrame,
        ignore_order: bool = True,
    ) -> DataComparisonResult:
        """
        Compare column names between actual and expected.
        """
        actual_cols = list(actual.columns)
        expected_cols = list(expected.columns)

        if ignore_order:
            actual_set = set(actual_cols)
            expected_set = set(expected_cols)

            missing_in_actual = list(expected_set - actual_set)
            extra_in_actual = list(actual_set - expected_set)

            if not missing_in_actual and not extra_in_actual:
                return DataComparisonResult(
                    success=True,
                    message="Schema/columns match (order ignored).",
                    meta={
                        "actual_columns": actual_cols,
                        "expected_columns": expected_cols,
                    },
                )

            details = {
                "missing_in_actual": missing_in_actual,
                "extra_in_actual": extra_in_actual,
            }
            return DataComparisonResult(
                success=False,
                message="Schema mismatch.",
                meta=details,
            )

        # order-sensitive comparison
        if actual_cols == expected_cols:
            return DataComparisonResult(
                success=True,
                message="Schema/columns match (order sensitive).",
                meta={
                    "actual_columns": actual_cols,
                    "expected_columns": expected_cols,
                },
            )

        return DataComparisonResult(
            success=False,
            message="Schema mismatch (order sensitive).",
            meta={
                "actual_columns": actual_cols,
                "expected_columns": expected_cols,
            },
        )

    def compare_by_keys(
        self,
        actual: pd.DataFrame,
        expected: pd.DataFrame,
        key_columns: List[str],
        value_columns: Optional[List[str]] = None,
        numeric_tolerance: float = 0.0,
    ) -> DataComparisonResult:
        """
        Compare two DataFrames by joining on key columns and checking value columns.
        Uses full outer join with indicator to find:
        - Missing in actual
        - Missing in expected
        - Mismatched values for common keys
        """

        # Ensure keys exist
        for col in key_columns:
            if col not in actual.columns:
                return DataComparisonResult(
                    success=False,
                    message=f"Key column '{col}' missing in actual DataFrame.",
                )
            if col not in expected.columns:
                return DataComparisonResult(
                    success=False,
                    message=f"Key column '{col}' missing in expected DataFrame.",
                )

        # Decide which value columns to compare
        if value_columns is None:
            # Common non-key columns
            common_cols = (
                set(actual.columns) & set(expected.columns)
            ) - set(key_columns)
            value_columns = sorted(list(common_cols))

        # Suffixes for merged columns
        suffixes = ("_actual", "_expected")

        merged = actual.merge(
            expected,
            on=key_columns,
            how="outer",
            indicator=True,
            suffixes=suffixes,
        )

        # Missing in each side
        missing_in_actual = merged[merged["_merge"] == "right_only"]
        missing_in_expected = merged[merged["_merge"] == "left_only"]

        mismatched_rows = []

        # Only check rows present in both
        both = merged[merged["_merge"] == "both"].copy()

        for col in value_columns:
            col_actual = f"{col}{suffixes[0]}"
            col_expected = f"{col}{suffixes[1]}"

            if col_actual not in both.columns or col_expected not in both.columns:
                continue

            if pd.api.types.is_numeric_dtype(both[col_actual]) and pd.api.types.is_numeric_dtype(
                both[col_expected]
            ):
                diff_series = (both[col_actual] - both[col_expected]).abs()
                mask = diff_series > numeric_tolerance
            else:
                mask = both[col_actual] != both[col_expected]

            if mask.any():
                diff_df = both.loc[mask, key_columns + [col_actual, col_expected]].copy()
                diff_df["COLUMN_NAME"] = col
                mismatched_rows.append(diff_df)

        mismatched_df = (
            pd.concat(mismatched_rows, ignore_index=True) if mismatched_rows else pd.DataFrame()
        )

        if missing_in_actual.empty and missing_in_expected.empty and mismatched_df.empty:
            return DataComparisonResult(
                success=True,
                message="Data matches for all key and value columns.",
            )

        # Build a details object for reporting
        details_meta: Dict[str, Any] = {
            "missing_in_actual_count": len(missing_in_actual),
            "missing_in_expected_count": len(missing_in_expected),
            "mismatched_count": len(mismatched_df),
        }

        # Optionally store a combined details DataFrame (can be large, so keep optional)
        details_df_list = []

        if not missing_in_actual.empty:
            tmp = missing_in_actual[key_columns].copy()
            tmp["ISSUE_TYPE"] = "MISSING_IN_ACTUAL"
            details_df_list.append(tmp)

        if not missing_in_expected.empty:
            tmp = missing_in_expected[key_columns].copy()
            tmp["ISSUE_TYPE"] = "MISSING_IN_EXPECTED"
            details_df_list.append(tmp)

        if not mismatched_df.empty:
            tmp = mismatched_df.copy()
            tmp["ISSUE_TYPE"] = "VALUE_MISMATCH"
            details_df_list.append(tmp)

        combined_details_df = (
            pd.concat(details_df_list, ignore_index=True) if details_df_list else None
        )

        return DataComparisonResult(
            success=False,
            message="Data mismatch detected. "
                    f"Missing in actual={len(missing_in_actual)}, "
                    f"Missing in expected={len(missing_in_expected)}, "
                    f"Value mismatches={len(mismatched_df)}.",
            details=combined_details_df,
            meta=details_meta,
        )
