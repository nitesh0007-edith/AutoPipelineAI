"""
Memory Store - In-memory storage for session data and conversation history
"""
from typing import Any, Dict, List, Optional
from datetime import datetime
from loguru import logger
import json


class MemoryStore:
    """In-memory store for session data, conversation history, and context"""

    def __init__(self, max_history: int = 100):
        """
        Initialize memory store

        Args:
            max_history: Maximum number of history entries to keep
        """
        self.max_history = max_history

        # Conversation history
        self.conversation_history: List[Dict[str, Any]] = []

        # Session data
        self.session_data: Dict[str, Any] = {}

        # User context
        self.user_context: Dict[str, Any] = {}

        # Execution logs
        self.execution_logs: List[Dict[str, Any]] = []

        logger.info(f"Initialized MemoryStore with max_history: {max_history}")

    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Add message to conversation history

        Args:
            role: Message role (user, assistant, system)
            content: Message content
            metadata: Optional metadata
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }

        self.conversation_history.append(message)

        # Trim history if needed
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]

        logger.debug(f"Added {role} message to history")

    def get_conversation_history(
        self,
        limit: Optional[int] = None,
        role_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get conversation history

        Args:
            limit: Maximum number of messages to return
            role_filter: Filter by role (user, assistant, system)

        Returns:
            List of messages
        """
        history = self.conversation_history

        if role_filter:
            history = [msg for msg in history if msg["role"] == role_filter]

        if limit:
            history = history[-limit:]

        return history

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history.clear()
        logger.info("Cleared conversation history")

    def set_session_data(self, key: str, value: Any):
        """
        Set session data

        Args:
            key: Data key
            value: Data value
        """
        self.session_data[key] = value
        logger.debug(f"Set session data: {key}")

    def get_session_data(self, key: str, default: Any = None) -> Any:
        """
        Get session data

        Args:
            key: Data key
            default: Default value if key not found

        Returns:
            Session data value
        """
        return self.session_data.get(key, default)

    def update_session_data(self, data: Dict[str, Any]):
        """
        Update multiple session data entries

        Args:
            data: Dictionary of key-value pairs
        """
        self.session_data.update(data)
        logger.debug(f"Updated {len(data)} session data entries")

    def clear_session_data(self):
        """Clear all session data"""
        self.session_data.clear()
        logger.info("Cleared session data")

    def set_context(self, key: str, value: Any):
        """
        Set user context

        Args:
            key: Context key
            value: Context value
        """
        self.user_context[key] = value
        logger.debug(f"Set context: {key}")

    def get_context(self, key: str, default: Any = None) -> Any:
        """
        Get user context

        Args:
            key: Context key
            default: Default value if key not found

        Returns:
            Context value
        """
        return self.user_context.get(key, default)

    def get_all_context(self) -> Dict[str, Any]:
        """
        Get all user context

        Returns:
            Dictionary of all context
        """
        return self.user_context.copy()

    def clear_context(self):
        """Clear user context"""
        self.user_context.clear()
        logger.info("Cleared user context")

    def log_execution(
        self,
        operation: str,
        status: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Log execution event

        Args:
            operation: Operation name
            status: Status (success, error, warning)
            details: Optional details dictionary
        """
        log_entry = {
            "operation": operation,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }

        self.execution_logs.append(log_entry)

        # Trim logs if needed
        if len(self.execution_logs) > self.max_history:
            self.execution_logs = self.execution_logs[-self.max_history:]

        logger.debug(f"Logged execution: {operation} - {status}")

    def get_execution_logs(
        self,
        limit: Optional[int] = None,
        status_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get execution logs

        Args:
            limit: Maximum number of logs to return
            status_filter: Filter by status

        Returns:
            List of log entries
        """
        logs = self.execution_logs

        if status_filter:
            logs = [log for log in logs if log["status"] == status_filter]

        if limit:
            logs = logs[-limit:]

        return logs

    def clear_execution_logs(self):
        """Clear execution logs"""
        self.execution_logs.clear()
        logger.info("Cleared execution logs")

    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary of memory store

        Returns:
            Dictionary with summary statistics
        """
        return {
            "conversation_messages": len(self.conversation_history),
            "session_data_keys": len(self.session_data),
            "context_keys": len(self.user_context),
            "execution_logs": len(self.execution_logs),
            "max_history": self.max_history
        }

    def export_to_json(self, file_path: str) -> bool:
        """
        Export memory store to JSON file

        Args:
            file_path: Output file path

        Returns:
            True if successful
        """
        try:
            data = {
                "conversation_history": self.conversation_history,
                "session_data": self.session_data,
                "user_context": self.user_context,
                "execution_logs": self.execution_logs,
                "exported_at": datetime.now().isoformat()
            }

            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)

            logger.info(f"Exported memory store to {file_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to export memory store: {e}")
            return False

    def import_from_json(self, file_path: str) -> bool:
        """
        Import memory store from JSON file

        Args:
            file_path: Input file path

        Returns:
            True if successful
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            self.conversation_history = data.get("conversation_history", [])
            self.session_data = data.get("session_data", {})
            self.user_context = data.get("user_context", {})
            self.execution_logs = data.get("execution_logs", [])

            logger.info(f"Imported memory store from {file_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to import memory store: {e}")
            return False

    def clear_all(self):
        """Clear all data in memory store"""
        self.clear_history()
        self.clear_session_data()
        self.clear_context()
        self.clear_execution_logs()
        logger.info("Cleared all memory store data")
