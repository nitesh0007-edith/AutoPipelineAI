"""
Profiling Agent - Specialized in data profiling and quality assessment
"""
from typing import Any, Dict, Optional
import pandas as pd
from loguru import logger

from .base_agent import BaseAgent
from src.utils.profiling import generate_profile


class ProfilingAgent(BaseAgent):
    """Agent specialized in data profiling and quality checks"""

    def __init__(self):
        super().__init__(
            name="Profiling Agent",
            description="Generates data profiles and quality reports"
        )

    def can_handle(self, task: Dict[str, Any]) -> bool:
        """
        Check if task is a profiling operation

        Args:
            task: Task dictionary

        Returns:
            True if task type is 'profile' or contains profiling keywords
        """
        task_type = task.get("type", "").lower()
        description = task.get("description", "").lower()

        profiling_keywords = ["profile", "quality", "summary", "statistics", "report", "describe"]

        return task_type == "profile" or any(keyword in description for keyword in profiling_keywords)

    def execute(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute profiling task

        Args:
            task: Task with optional output_path
            context: Context with 'df' DataFrame

        Returns:
            Result dictionary with profile information
        """
        try:
            if not context or "df" not in context:
                return {
                    "success": False,
                    "data": None,
                    "error": "No DataFrame provided in context"
                }

            df = context["df"]
            output_path = task.get("output_path", "data/reports/profile.html")

            # Generate comprehensive profile
            logger.info(f"Generating profile report for DataFrame with {len(df)} rows")
            generate_profile(df, output_path)

            # Also generate quick stats
            stats = self._generate_quick_stats(df)

            result = {
                "success": True,
                "data": stats,
                "error": None,
                "metadata": {
                    "report_path": output_path,
                    "rows": len(df),
                    "columns": len(df.columns)
                }
            }

            self.log_execution(task, result)
            return result

        except Exception as e:
            logger.error(f"Profiling execution failed: {e}")
            result = {
                "success": False,
                "data": None,
                "error": str(e)
            }
            self.log_execution(task, result)
            return result

    def _generate_quick_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate quick statistics about the DataFrame

        Args:
            df: DataFrame to analyze

        Returns:
            Dictionary with quick stats
        """
        stats = {
            "shape": {"rows": len(df), "columns": len(df.columns)},
            "columns": list(df.columns),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "missing_percentage": (df.isnull().sum() / len(df) * 100).to_dict(),
            "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024**2
        }

        # Numeric columns statistics
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            stats["numeric_summary"] = df[numeric_cols].describe().to_dict()

        # Categorical columns info
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0:
            stats["categorical_info"] = {
                col: {
                    "unique_count": df[col].nunique(),
                    "top_values": df[col].value_counts().head(5).to_dict()
                }
                for col in categorical_cols
            }

        return stats
