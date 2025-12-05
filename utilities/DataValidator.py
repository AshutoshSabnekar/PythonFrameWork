from typing import List, Optional, Dict, Any
import pandas as pd

from .DataComparator import DataComparator, DataComparisonResult
from .SemanticViewDataFetcher import SemanticViewDataFetcher


class DataValidator:
    """
    Orchestrates semantic-view validations using SemanticViewDataFetcher and DataComparator.
    You can call these methods from your test cases.
    """

    def __init__(
        self,
        fetcher: SemanticViewDataFetcher,
        comparator: Optional[DataComparator] = None,
    ):
        self.fetcher = fetcher
        self.comparator = comparator or DataComparator()

    def validate_row_count(
        self,
        view_name: str,
        expected_df: pd.DataFrame,
        filters: Optional[str] = None,
        tolerance: int = 0,
    ) -> DataComparisonResult:
        """
        Fetches the semantic view and compares its row count with expected_df.
        """
        actual_df = self.fetcher.fetch_view_data(
            view_name=view_name,
            filters=filters,
        )
        return self.comparator.compare_row_count(
            actual=actual_df,
            expected=expected_df,
            tolerance=tolerance,
        )

    def validate_schema(
        self,
        view_name: str,
        expected_df: pd.DataFrame,
        filters: Optional[str] = None,
        ignore_order: bool = True,
    ) -> DataComparisonResult:
        """
        Fetches the semantic view and compares schema/columns with expected_df.
        """
        actual_df = self.fetcher.fetch_view_data(
            view_name=view_name,
            filters=filters,
            limit=1,  # enough to get schema
        )
        return self.comparator.compare_schema(
            actual=actual_df,
            expected=expected_df,
            ignore_order=ignore_order,
        )

    def validate_data_by_keys(
        self,
        view_name: str,
        expected_df: pd.DataFrame,
        key_columns: List[str],
        value_columns: Optional[List[str]] = None,
        filters: Optional[str] = None,
        numeric_tolerance: float = 0.0,
        limit: Optional[int] = None,
    ) -> DataComparisonResult:
        """
        Full data validation for a semantic view:
        - Fetches actual data from the view
        - Compares against expected_df on keys and value columns
        """
        actual_df = self.fetcher.fetch_view_data(
            view_name=view_name,
            filters=filters,
            limit=limit,
        )

        return self.comparator.compare_by_keys(
            actual=actual_df,
            expected=expected_df,
            key_columns=key_columns,
            value_columns=value_columns,
            numeric_tolerance=numeric_tolerance,
        )

    def validate_against_source(
        self,
        source_df: pd.DataFrame,
        view_name: str,
        key_columns: List[str],
        value_columns: Optional[List[str]] = None,
        source_filters: Optional[str] = None,
        view_filters: Optional[str] = None,
        numeric_tolerance: float = 0.0,
        limit: Optional[int] = None,
    ) -> DataComparisonResult:
        """
        Pattern for 'source vs semantic view' validation where:
        - source_df is the already extracted source data DataFrame
        - semantic view is fetched and compared
        """
        # Optionally you can apply extra filters to source_df here if needed
        # For now, we assume source_df is already filtered.

        actual_view_df = self.fetcher.fetch_view_data(
            view_name=view_name,
            filters=view_filters,
            limit=limit,
        )

        return self.comparator.compare_by_keys(
            actual=actual_view_df,
            expected=source_df,
            key_columns=key_columns,
            value_columns=value_columns,
            numeric_tolerance=numeric_tolerance,
        )
