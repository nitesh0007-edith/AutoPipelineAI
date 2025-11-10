"""
Tests for LLM Module
"""
import unittest
import pandas as pd

from src.llm.code_executor import SafeCodeExecutor
from src.llm.prompt_templates import PromptTemplates


class TestSafeCodeExecutor(unittest.TestCase):
    """Test SafeCodeExecutor functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.executor = SafeCodeExecutor()

    def test_extract_code_blocks(self):
        """Test extracting code from markdown"""
        text = """
        Here's some code:
        ```python
        result = 1 + 1
        ```
        """
        blocks = self.executor.extract_code_blocks(text)
        self.assertEqual(len(blocks), 1)
        self.assertIn("result = 1 + 1", blocks[0])

    def test_check_code_safety_safe(self):
        """Test safety check for safe code"""
        safe_code = "result = 1 + 1"
        is_safe, error = self.executor.check_code_safety(safe_code)
        self.assertTrue(is_safe)
        self.assertIsNone(error)

    def test_check_code_safety_unsafe(self):
        """Test safety check for unsafe code"""
        unsafe_code = "import os; os.system('ls')"
        is_safe, error = self.executor.check_code_safety(unsafe_code)
        self.assertFalse(is_safe)
        self.assertIsNotNone(error)

    def test_execute_code_success(self):
        """Test successful code execution"""
        code = "result = 2 + 2"
        result = self.executor.execute_code(code)

        self.assertTrue(result["success"])
        self.assertEqual(result["result"], 4)

    def test_execute_code_with_context(self):
        """Test code execution with context"""
        df = pd.DataFrame({"a": [1, 2, 3]})
        code = "result = df['a'].sum()"

        result = self.executor.execute_code(code, context={"df": df})

        self.assertTrue(result["success"])
        self.assertEqual(result["result"], 6)

    def test_execute_code_error(self):
        """Test code execution with error"""
        code = "result = undefined_variable"
        result = self.executor.execute_code(code)

        self.assertFalse(result["success"])
        self.assertIsNotNone(result["error"])


class TestPromptTemplates(unittest.TestCase):
    """Test PromptTemplates functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.df = pd.DataFrame({
            "product": ["A", "B", "C"],
            "sales": [100, 200, 300]
        })

    def test_data_analysis_prompt(self):
        """Test data analysis prompt generation"""
        prompt = PromptTemplates.data_analysis_prompt(
            self.df,
            "What is the total sales?"
        )

        self.assertIn("Total Rows: 3", prompt)
        self.assertIn("Total Columns: 2", prompt)
        self.assertIn("What is the total sales?", prompt)

    def test_etl_task_prompt(self):
        """Test ETL task prompt generation"""
        prompt = PromptTemplates.etl_task_prompt(
            "Load and clean data",
            ["file1.csv", "file2.csv"],
            "CSV"
        )

        self.assertIn("file1.csv", prompt)
        self.assertIn("Load and clean data", prompt)
        self.assertIn("CSV", prompt)

    def test_sql_generation_prompt(self):
        """Test SQL generation prompt"""
        schema = {"users": "id INT, name TEXT"}
        prompt = PromptTemplates.sql_generation_prompt(
            schema,
            "Get all users",
            "DuckDB"
        )

        self.assertIn("users", prompt)
        self.assertIn("Get all users", prompt)
        self.assertIn("DuckDB", prompt)


if __name__ == "__main__":
    unittest.main()
