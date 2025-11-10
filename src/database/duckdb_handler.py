"""
DuckDB Handler - Efficient analytical database for DataFrames
"""
import duckdb
import pandas as pd
from typing import Optional, List, Dict, Any
from loguru import logger
from pathlib import Path


class DuckDBHandler:
    """Handler for DuckDB database operations"""

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize DuckDB handler

        Args:
            db_path: Path to database file. If None, uses in-memory database.
        """
        self.db_path = db_path or ":memory:"
        self.conn = duckdb.connect(self.db_path)
        logger.info(f"Connected to DuckDB: {self.db_path}")

    def create_table_from_df(self, df: pd.DataFrame, table_name: str, if_exists: str = "replace") -> bool:
        """
        Create table from DataFrame

        Args:
            df: Source DataFrame
            table_name: Name for the table
            if_exists: 'replace' or 'append'

        Returns:
            True if successful
        """
        try:
            if if_exists == "replace":
                self.conn.execute(f"DROP TABLE IF EXISTS {table_name}")

            self.conn.register(table_name, df)
            self.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM {table_name}")

            logger.info(f"Created table '{table_name}' with {len(df)} rows")
            return True

        except Exception as e:
            logger.error(f"Failed to create table: {e}")
            return False

    def query(self, sql: str) -> pd.DataFrame:
        """
        Execute SQL query and return result as DataFrame

        Args:
            sql: SQL query string

        Returns:
            Query result as DataFrame
        """
        try:
            result = self.conn.execute(sql).fetchdf()
            logger.info(f"Query executed successfully, returned {len(result)} rows")
            return result

        except Exception as e:
            logger.error(f"Query failed: {e}")
            raise

    def execute(self, sql: str) -> bool:
        """
        Execute SQL statement (INSERT, UPDATE, DELETE, etc.)

        Args:
            sql: SQL statement

        Returns:
            True if successful
        """
        try:
            self.conn.execute(sql)
            logger.info("SQL statement executed successfully")
            return True

        except Exception as e:
            logger.error(f"SQL execution failed: {e}")
            return False

    def list_tables(self) -> List[str]:
        """
        List all tables in database

        Returns:
            List of table names
        """
        try:
            result = self.conn.execute("SHOW TABLES").fetchall()
            tables = [row[0] for row in result]
            logger.info(f"Found {len(tables)} tables")
            return tables

        except Exception as e:
            logger.error(f"Failed to list tables: {e}")
            return []

    def get_table_schema(self, table_name: str) -> pd.DataFrame:
        """
        Get schema information for a table

        Args:
            table_name: Name of the table

        Returns:
            DataFrame with schema information
        """
        try:
            result = self.conn.execute(f"DESCRIBE {table_name}").fetchdf()
            return result

        except Exception as e:
            logger.error(f"Failed to get schema: {e}")
            raise

    def insert_dataframe(self, df: pd.DataFrame, table_name: str) -> bool:
        """
        Insert DataFrame into existing table

        Args:
            df: DataFrame to insert
            table_name: Target table name

        Returns:
            True if successful
        """
        try:
            self.conn.register("temp_df", df)
            self.conn.execute(f"INSERT INTO {table_name} SELECT * FROM temp_df")
            self.conn.unregister("temp_df")

            logger.info(f"Inserted {len(df)} rows into '{table_name}'")
            return True

        except Exception as e:
            logger.error(f"Failed to insert data: {e}")
            return False

    def read_csv(self, csv_path: str, table_name: Optional[str] = None) -> pd.DataFrame:
        """
        Read CSV file directly with DuckDB (very fast)

        Args:
            csv_path: Path to CSV file
            table_name: Optional table name to create

        Returns:
            DataFrame with CSV data
        """
        try:
            query = f"SELECT * FROM read_csv_auto('{csv_path}')"
            result = self.conn.execute(query).fetchdf()

            if table_name:
                self.create_table_from_df(result, table_name)

            logger.info(f"Read {len(result)} rows from CSV")
            return result

        except Exception as e:
            logger.error(f"Failed to read CSV: {e}")
            raise

    def read_parquet(self, parquet_path: str, table_name: Optional[str] = None) -> pd.DataFrame:
        """
        Read Parquet file directly with DuckDB

        Args:
            parquet_path: Path to Parquet file
            table_name: Optional table name to create

        Returns:
            DataFrame with Parquet data
        """
        try:
            query = f"SELECT * FROM read_parquet('{parquet_path}')"
            result = self.conn.execute(query).fetchdf()

            if table_name:
                self.create_table_from_df(result, table_name)

            logger.info(f"Read {len(result)} rows from Parquet")
            return result

        except Exception as e:
            logger.error(f"Failed to read Parquet: {e}")
            raise

    def export_to_parquet(self, table_name: str, output_path: str) -> bool:
        """
        Export table to Parquet file

        Args:
            table_name: Source table name
            output_path: Output file path

        Returns:
            True if successful
        """
        try:
            self.conn.execute(f"COPY {table_name} TO '{output_path}' (FORMAT PARQUET)")
            logger.info(f"Exported table '{table_name}' to {output_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to export to Parquet: {e}")
            return False

    def aggregate_stats(self, table_name: str) -> Dict[str, Any]:
        """
        Get aggregate statistics for a table

        Args:
            table_name: Table name

        Returns:
            Dictionary with statistics
        """
        try:
            # Row count
            row_count = self.conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]

            # Schema
            schema = self.get_table_schema(table_name)

            # Column statistics for numeric columns
            numeric_cols = schema[schema['column_type'].str.contains('INT|DOUBLE|DECIMAL|FLOAT', regex=True)]['column_name'].tolist()

            stats = {
                "row_count": row_count,
                "column_count": len(schema),
                "columns": schema.to_dict('records'),
                "numeric_stats": {}
            }

            for col in numeric_cols[:10]:  # Limit to first 10 numeric columns
                col_stats = self.conn.execute(f"""
                    SELECT
                        MIN({col}) as min,
                        MAX({col}) as max,
                        AVG({col}) as avg,
                        STDDEV({col}) as stddev
                    FROM {table_name}
                """).fetchone()

                stats["numeric_stats"][col] = {
                    "min": col_stats[0],
                    "max": col_stats[1],
                    "avg": col_stats[2],
                    "stddev": col_stats[3]
                }

            return stats

        except Exception as e:
            logger.error(f"Failed to compute stats: {e}")
            return {}

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("DuckDB connection closed")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
