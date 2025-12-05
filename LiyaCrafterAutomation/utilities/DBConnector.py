import pyodbc
import snowflake.connector
from databricks import sql as databricks_sql
import cx_Oracle
import pandas as pd

class MultiDBConnectionManager:
    def __init__(self, db_type, config):
        self.db_type = db_type.lower()
        self.config = config
        self.conn = None

    def connect(self):
        if self.db_type == 'azure_sql':
            conn_str = self.config.get('connection_string')
            self.conn = pyodbc.connect(conn_str)
        elif self.db_type == 'snowflake':
            self.conn = snowflake.connector.connect(
                user=self.config.get('user'),
                password=self.config.get('password'),
                account=self.config.get('account'),
                warehouse=self.config.get('warehouse'),
                database=self.config.get('database'),
                schema=self.config.get('schema')
            )
        elif self.db_type == 'databricks':
            self.conn = databricks_sql.connect(
                server_hostname=self.config.get('server_hostname'),
                http_path=self.config.get('http_path'),
                access_token=self.config.get('access_token')
            )
        elif self.db_type == 'oracle':
            dsn = cx_Oracle.makedsn(
                self.config.get('host'), self.config.get('port'), service_name=self.config.get('service_name')
            )
            self.conn = cx_Oracle.connect(
                user=self.config.get('user'),
                password=self.config.get('password'),
                dsn=dsn
            )
        elif self.db_type == 'lakehouse':
            # Connect using appropriate connector or API (e.g., Databricks Lakehouse)
            pass
        else:
            raise ValueError(f"Unsupported DB type: {self.db_type}")

    def execute_query(self, query):
        if not self.conn:
            self.connect()
        if self.db_type in ['azure_sql', 'oracle']:
            return pd.read_sql(query, self.conn)
        elif self.db_type == 'snowflake':
            cursor = self.conn.cursor()
            cursor.execute(query)
            df = pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description])
            cursor.close()
            return df
        elif self.db_type == 'databricks':
            cursor = self.conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            cursor.close()
            return pd.DataFrame(rows, columns=columns)
        else:
            # Implement other DB query executions
            pass

    def close(self):
        if self.conn:
            if self.db_type in ['snowflake', 'databricks']:
                self.conn.close()
            else:
                self.conn.close()
            self.conn = None
