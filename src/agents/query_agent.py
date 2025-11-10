"""
Query Agent - Specialized in answering data queries using LLM
"""
from typing import Any, Dict, Optional
import pandas as pd
from loguru import logger

from .base_agent import BaseAgent
from src.llm.ollama_client import OllamaClient
from src.llm.prompt_templates import PromptTemplates
from src.llm.code_executor import SafeCodeExecutor


class QueryAgent(BaseAgent):
    """Agent specialized in answering natural language queries about data"""

    def __init__(self, llm_client: Optional[OllamaClient] = None):
        super().__init__(
            name="Query Agent",
            description="Answers natural language questions about data using LLM"
        )
        self.llm_client = llm_client or OllamaClient()
        self.code_executor = SafeCodeExecutor()

    def can_handle(self, task: Dict[str, Any]) -> bool:
        """
        Check if task is a query operation

        Args:
            task: Task dictionary

        Returns:
            True if task type is 'query' or contains query keywords
        """
        task_type = task.get("type", "").lower()
        description = task.get("description", "").lower()

        query_keywords = ["query", "question", "analyze", "what", "how", "show", "find", "get"]

        return task_type == "query" or any(keyword in description for keyword in query_keywords)

    def execute(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute query task using LLM

        Args:
            task: Task with 'query' field
            context: Context with 'df' DataFrame

        Returns:
            Result dictionary with answer and data
        """
        try:
            query = task.get("query") or task.get("description")
            model = task.get("model", "llama3")

            if not context or "df" not in context:
                return {
                    "success": False,
                    "data": None,
                    "error": "No DataFrame provided in context"
                }

            df = context["df"]

            # Generate prompt using template
            prompt = PromptTemplates.data_analysis_prompt(df, query)

            # Get LLM response
            logger.info(f"Sending query to LLM: {query}")
            llm_response = self.llm_client.generate_completion(
                prompt=prompt,
                model=model,
                temperature=0.4
            )

            # Execute code from response
            exec_result = self.code_executor.execute_from_llm_response(
                llm_response,
                context={"df": df, "pd": pd}
            )

            result = {
                "success": exec_result["success"],
                "data": exec_result["result"],
                "llm_response": llm_response,
                "output": exec_result["output"],
                "error": exec_result["error"]
            }

            self.log_execution(task, result)
            return result

        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            result = {
                "success": False,
                "data": None,
                "error": str(e)
            }
            self.log_execution(task, result)
            return result
