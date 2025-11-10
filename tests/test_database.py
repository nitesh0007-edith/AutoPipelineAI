"""
Tests for Database Module
"""
import unittest
import tempfile
import pandas as pd
from pathlib import Path

from src.database.duckdb_handler import DuckDBHandler
from src.database.sqlite_handler import SQLiteHandler


class TestDuckDBHandler(unittest.TestCase):
    """Test DuckDB Handler functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.db = DuckDBHandler()  # In-memory database
        self.test_df = pd.DataFrame({
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "value": [100, 200, 300]
        })

    def tearDown(self):
        """Clean up"""
        self.db.close()

    def test_create_table(self):
        """Test creating table from DataFrame"""
        result = self.db.create_table_from_df(self.test_df, "test_table")
        self.assertTrue(result)

        tables = self.db.list_tables()
        self.assertIn("test_table", tables)

    def test_query(self):
        """Test querying data"""
        self.db.create_table_from_df(self.test_df, "test_table")
        result = self.db.query("SELECT * FROM test_table WHERE value > 100")
        self.assertEqual(len(result), 2)

    def test_insert_dataframe(self):
        """Test inserting DataFrame"""
        self.db.create_table_from_df(self.test_df, "test_table")

        new_df = pd.DataFrame({
            "id": [4],
            "name": ["David"],
            "value": [400]
        })

        self.db.insert_dataframe(new_df, "test_table")

        result = self.db.query("SELECT COUNT(*) as count FROM test_table")
        self.assertEqual(result.iloc[0]["count"], 4)


class TestSQLiteHandler(unittest.TestCase):
    """Test SQLite Handler functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db = SQLiteHandler(self.temp_db.name)
        self.test_df = pd.DataFrame({
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "value": [100, 200, 300]
        })

    def tearDown(self):
        """Clean up"""
        self.db.close()
        Path(self.temp_db.name).unlink(missing_ok=True)

    def test_create_table(self):
        """Test creating table from DataFrame"""
        result = self.db.create_table_from_df(self.test_df, "test_table")
        self.assertTrue(result)

        tables = self.db.list_tables()
        self.assertIn("test_table", tables)

    def test_query(self):
        """Test querying data"""
        self.db.create_table_from_df(self.test_df, "test_table")
        result = self.db.query("SELECT * FROM test_table WHERE value > 100")
        self.assertEqual(len(result), 2)

    def test_get_table_schema(self):
        """Test getting table schema"""
        self.db.create_table_from_df(self.test_df, "test_table")
        schema = self.db.get_table_schema("test_table")
        self.assertEqual(len(schema), 3)  # 3 columns

    def test_row_count(self):
        """Test getting row count"""
        self.db.create_table_from_df(self.test_df, "test_table")
        count = self.db.get_table_row_count("test_table")
        self.assertEqual(count, 3)


if __name__ == "__main__":
    unittest.main()
