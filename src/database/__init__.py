"""
Database Module - SQLite and DuckDB support
"""
from .duckdb_handler import DuckDBHandler
from .sqlite_handler import SQLiteHandler

__all__ = ['DuckDBHandler', 'SQLiteHandler']
