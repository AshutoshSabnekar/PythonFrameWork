from typing import Dict, List, Optional
import pandas as pd

class SemanticViewDataFetcher:
    """
    Generic data fetcher for semantic views across multiple databases.
    Expects a connection manager with an execute_query(sql: str) -> pd.DataFrame method.
    """

    def __init__(self, connection_manager):
        """
        :param connection_manager: Instance of your MultiDBConnectionManager (or similar)
        """
        self.conn_mgr = connection_manager

    def _build_select_query(
        self,
        view_name: str,
        columns: Optional[List[str]] = None,
        filters: Optional[str] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> str:
        """
        Builds a simple SELECT query for a semantic view.
        You can extend this if you need DB-specific syntax.
        """

        col_expr = ", ".join(columns) if columns else "*"
        query = f"SELECT {col_expr} FROM {view_name}"

        if filters:
            query += f" WHERE {filters}"

        if order_by:
            query += f" ORDER BY {order_by}"

        # Most DBs support LIMIT; for Oracle you can override this method or wrap it.
        if limit is not None:
            if self.conn_mgr.db_type.lower() in ["oracle"]:
                # Example Oracle style; adapt if you use ROWNUM or FETCH FIRST.
                query = f"SELECT * FROM ({query}) WHERE ROWNUM <= {limit}"
            else:
                query += f" LIMIT {limit}"

        return query

    def fetch_view_data(
        self,
        view_name: str,
        columns: Optional[List[str]] = None,
        filters: Optional[str] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> pd.DataFrame:
        """
        Fetches data from a semantic view as a pandas DataFrame.
        """
        sql = self._build_select_query(
            view_name=view_name,
            columns=columns,
            filters=filters,
            order_by=order_by,
            limit=limit,
        )
        return self.conn_mgr.execute_query(sql)

    def fetch_row_count(self, view_name: str, filters: Optional[str] = None) -> int:
        """
        Quickly get row count for a view, optionally with filters.
        Useful for validations like 'semantic view vs source row counts'.
        """
        query = f"SELECT COUNT(1) AS ROW_COUNT FROM {view_name}"
        if filters:
            query += f" WHERE {filters}"
        df = self.conn_mgr.execute_query(query)
        return int(df.iloc[0]["ROW_COUNT"])

    def fetch_distinct_values(
        self,
        view_name: str,
        column_name: str,
        filters: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> pd.DataFrame:
        """
        Fetch distinct values for a column in a semantic view.
        Useful for validating domains, lookups, etc.
        """
        base_query = f"SELECT DISTINCT {column_name} FROM {view_name}"
        if filters:
            base_query += f" WHERE {filters}"

        if limit is not None:
            if self.conn_mgr.db_type.lower() == "oracle":
                base_query = f"SELECT * FROM ({base_query}) WHERE ROWNUM <= {limit}"
            else:
                base_query += f" LIMIT {limit}"

        return self.conn_mgr.execute_query(base_query)
