"""
SQLite Handler - Lightweight relational database support
"""
import sqlite3
import pandas as pd
from typing import Optional, List, Dict, Any
from loguru import logger
from pathlib import Path


class SQLiteHandler:
    """Handler for SQLite database operations"""

    def __init__(self, db_path: str = "data/database.db"):
        """
        Initialize SQLite handler

        Args:
            db_path: Path to database file
        """
        self.db_path = db_path

        # Ensure directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        logger.info(f"Connected to SQLite database: {db_path}")

    def create_table_from_df(self, df: pd.DataFrame, table_name: str, if_exists: str = "replace") -> bool:
        """
        Create table from DataFrame

        Args:
            df: Source DataFrame
            table_name: Name for the table
            if_exists: 'replace', 'append', or 'fail'

        Returns:
            True if successful
        """
        try:
            df.to_sql(table_name, self.conn, if_exists=if_exists, index=False)
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
            result = pd.read_sql_query(sql, self.conn)
            logger.info(f"Query executed successfully, returned {len(result)} rows")
            return result

        except Exception as e:
            logger.error(f"Query failed: {e}")
            raise

    def execute(self, sql: str, params: Optional[tuple] = None) -> bool:
        """
        Execute SQL statement (INSERT, UPDATE, DELETE, etc.)

        Args:
            sql: SQL statement
            params: Optional parameters for parameterized query

        Returns:
            True if successful
        """
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)

            self.conn.commit()
            logger.info("SQL statement executed successfully")
            return True

        except Exception as e:
            logger.error(f"SQL execution failed: {e}")
            self.conn.rollback()
            return False

    def execute_many(self, sql: str, params_list: List[tuple]) -> bool:
        """
        Execute many SQL statements with different parameters

        Args:
            sql: SQL statement template
            params_list: List of parameter tuples

        Returns:
            True if successful
        """
        try:
            self.cursor.executemany(sql, params_list)
            self.conn.commit()
            logger.info(f"Executed {len(params_list)} statements successfully")
            return True

        except Exception as e:
            logger.error(f"Batch execution failed: {e}")
            self.conn.rollback()
            return False

    def list_tables(self) -> List[str]:
        """
        List all tables in database

        Returns:
            List of table names
        """
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in self.cursor.fetchall()]
            logger.info(f"Found {len(tables)} tables")
            return tables

        except Exception as e:
            logger.error(f"Failed to list tables: {e}")
            return []

    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Get schema information for a table

        Args:
            table_name: Name of the table

        Returns:
            List of column information dictionaries
        """
        try:
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns = self.cursor.fetchall()

            schema = []
            for col in columns:
                schema.append({
                    "cid": col[0],
                    "name": col[1],
                    "type": col[2],
                    "notnull": bool(col[3]),
                    "default_value": col[4],
                    "primary_key": bool(col[5])
                })

            return schema

        except Exception as e:
            logger.error(f"Failed to get schema: {e}")
            raise

    def insert_dataframe(self, df: pd.DataFrame, table_name: str, if_exists: str = "append") -> bool:
        """
        Insert DataFrame into table

        Args:
            df: DataFrame to insert
            table_name: Target table name
            if_exists: 'replace', 'append', or 'fail'

        Returns:
            True if successful
        """
        try:
            df.to_sql(table_name, self.conn, if_exists=if_exists, index=False)
            logger.info(f"Inserted {len(df)} rows into '{table_name}'")
            return True

        except Exception as e:
            logger.error(f"Failed to insert data: {e}")
            return False

    def drop_table(self, table_name: str) -> bool:
        """
        Drop a table

        Args:
            table_name: Table name to drop

        Returns:
            True if successful
        """
        try:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.conn.commit()
            logger.info(f"Dropped table '{table_name}'")
            return True

        except Exception as e:
            logger.error(f"Failed to drop table: {e}")
            return False

    def vacuum(self) -> bool:
        """
        Vacuum database to reclaim space and optimize

        Returns:
            True if successful
        """
        try:
            self.cursor.execute("VACUUM")
            logger.info("Database vacuumed successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to vacuum database: {e}")
            return False

    def get_table_row_count(self, table_name: str) -> int:
        """
        Get row count for a table

        Args:
            table_name: Table name

        Returns:
            Number of rows
        """
        try:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = self.cursor.fetchone()[0]
            return count

        except Exception as e:
            logger.error(f"Failed to get row count: {e}")
            return 0

    def backup(self, backup_path: str) -> bool:
        """
        Create a backup of the database

        Args:
            backup_path: Path for backup file

        Returns:
            True if successful
        """
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            logger.info(f"Database backed up to {backup_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to backup database: {e}")
            return False

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("SQLite connection closed")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
