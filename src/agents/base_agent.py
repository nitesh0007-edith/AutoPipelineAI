"""
Base Agent - Abstract base class for all agents
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from loguru import logger
from datetime import datetime


class BaseAgent(ABC):
    """Abstract base class for all agents"""

    def __init__(self, name: str, description: str):
        """
        Initialize base agent

        Args:
            name: Agent name
            description: Agent description/purpose
        """
        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.execution_count = 0
        logger.info(f"Initialized agent: {name}")

    @abstractmethod
    def can_handle(self, task: Dict[str, Any]) -> bool:
        """
        Determine if this agent can handle the given task

        Args:
            task: Task dictionary with type, description, etc.

        Returns:
            True if agent can handle the task
        """
        pass

    @abstractmethod
    def execute(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute the task

        Args:
            task: Task to execute
            context: Optional execution context

        Returns:
            Result dictionary with success, data, error fields
        """
        pass

    def log_execution(self, task: Dict[str, Any], result: Dict[str, Any]):
        """
        Log task execution

        Args:
            task: Executed task
            result: Execution result
        """
        self.execution_count += 1
        status = "✅ SUCCESS" if result.get("success") else "❌ FAILED"
        logger.info(f"[{self.name}] {status} - Task: {task.get('type', 'unknown')}")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get agent statistics

        Returns:
            Dictionary with agent stats
        """
        return {
            "name": self.name,
            "description": self.description,
            "execution_count": self.execution_count,
            "created_at": self.created_at.isoformat()
        }
