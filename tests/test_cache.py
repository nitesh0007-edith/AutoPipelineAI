"""
Tests for Cache Module
"""
import unittest
import tempfile
import shutil
from pathlib import Path

from src.cache.cache_manager import CacheManager
from src.cache.memory_store import MemoryStore


class TestCacheManager(unittest.TestCase):
    """Test CacheManager functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.cache = CacheManager(cache_dir=self.temp_dir, ttl_seconds=10)

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)

    def test_memory_cache_set_get(self):
        """Test setting and getting from memory cache"""
        self.cache.set("test_key", "test_value", backend="memory")
        value = self.cache.get("test_key", backend="memory")
        self.assertEqual(value, "test_value")

    def test_disk_cache_set_get(self):
        """Test setting and getting from disk cache"""
        self.cache.set("test_key", {"data": "test"}, backend="disk")
        value = self.cache.get("test_key", backend="disk")
        self.assertEqual(value, {"data": "test"})

    def test_cache_miss(self):
        """Test cache miss returns None"""
        value = self.cache.get("nonexistent_key", backend="memory")
        self.assertIsNone(value)

    def test_cache_delete(self):
        """Test deleting from cache"""
        self.cache.set("test_key", "test_value", backend="memory")
        self.cache.delete("test_key", backend="memory")
        value = self.cache.get("test_key", backend="memory")
        self.assertIsNone(value)

    def test_cache_clear(self):
        """Test clearing all cache"""
        self.cache.set("key1", "value1", backend="memory")
        self.cache.set("key2", "value2", backend="disk")
        self.cache.clear(backend="both")

        self.assertIsNone(self.cache.get("key1", backend="memory"))
        self.assertIsNone(self.cache.get("key2", backend="disk"))


class TestMemoryStore(unittest.TestCase):
    """Test MemoryStore functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.store = MemoryStore(max_history=10)

    def test_add_message(self):
        """Test adding messages to history"""
        self.store.add_message("user", "Hello")
        history = self.store.get_conversation_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["role"], "user")
        self.assertEqual(history[0]["content"], "Hello")

    def test_session_data(self):
        """Test session data management"""
        self.store.set_session_data("key", "value")
        value = self.store.get_session_data("key")
        self.assertEqual(value, "value")

    def test_context_management(self):
        """Test context management"""
        self.store.set_context("user_id", 123)
        context = self.store.get_all_context()
        self.assertEqual(context["user_id"], 123)

    def test_execution_logging(self):
        """Test execution logging"""
        self.store.log_execution("test_op", "success", {"detail": "test"})
        logs = self.store.get_execution_logs()
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["operation"], "test_op")

    def test_clear_all(self):
        """Test clearing all data"""
        self.store.add_message("user", "test")
        self.store.set_session_data("key", "value")
        self.store.set_context("ctx", "val")
        self.store.log_execution("op", "success")

        self.store.clear_all()

        summary = self.store.get_summary()
        self.assertEqual(summary["conversation_messages"], 0)
        self.assertEqual(summary["session_data_keys"], 0)
        self.assertEqual(summary["context_keys"], 0)
        self.assertEqual(summary["execution_logs"], 0)


if __name__ == "__main__":
    unittest.main()
