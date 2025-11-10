"""
ETL Agent - Specialized in Extract, Transform, Load operations
"""
from typing import Any, Dict, Optional
import pandas as pd
from loguru import logger

from .base_agent import BaseAgent
from src.etl.load_superstore import load_and_clean_superstore, save_clean_data, filter_data


class ETLAgent(BaseAgent):
    """Agent specialized in ETL operations"""

    def __init__(self):
        super().__init__(
            name="ETL Agent",
            description="Handles data extraction, transformation, and loading operations"
        )

    def can_handle(self, task: Dict[str, Any]) -> bool:
        """
        Check if task is an ETL operation

        Args:
            task: Task dictionary

        Returns:
            True if task type is 'etl' or contains ETL keywords
        """
        task_type = task.get("type", "").lower()
        description = task.get("description", "").lower()

        etl_keywords = ["load", "extract", "transform", "clean", "filter", "save", "export"]

        return task_type == "etl" or any(keyword in description for keyword in etl_keywords)

    def execute(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute ETL task

        Args:
            task: Task with fields like file_path, operation, filters
            context: Optional context

        Returns:
            Result dictionary
        """
        try:
            operation = task.get("operation", "load")
            file_path = task.get("file_path")

            if operation == "load":
                result = self._load_data(file_path, task)
            elif operation == "transform":
                result = self._transform_data(task, context)
            elif operation == "save":
                result = self._save_data(task, context)
            elif operation == "filter":
                result = self._filter_data(task, context)
            else:
                result = {
                    "success": False,
                    "data": None,
                    "error": f"Unknown operation: {operation}"
                }

            self.log_execution(task, result)
            return result

        except Exception as e:
            logger.error(f"ETL execution failed: {e}")
            result = {
                "success": False,
                "data": None,
                "error": str(e)
            }
            self.log_execution(task, result)
            return result

    def _load_data(self, file_path: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """Load data from file"""
        try:
            if file_path.endswith('.csv'):
                # Check if it's superstore
                if "superstore" in file_path.lower():
                    df = load_and_clean_superstore(file_path)
                else:
                    encoding = task.get("encoding", "utf-8")
                    try:
                        df = pd.read_csv(file_path, encoding=encoding)
                    except UnicodeDecodeError:
                        df = pd.read_csv(file_path, encoding='latin1')
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            elif file_path.endswith('.parquet'):
                df = pd.read_parquet(file_path)
            else:
                return {
                    "success": False,
                    "data": None,
                    "error": f"Unsupported file format: {file_path}"
                }

            return {
                "success": True,
                "data": df,
                "error": None,
                "metadata": {
                    "rows": len(df),
                    "columns": len(df.columns),
                    "file": file_path
                }
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Failed to load data: {e}"
            }

    def _transform_data(self, task: Dict[str, Any], context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Apply transformations to data"""
        if not context or "df" not in context:
            return {
                "success": False,
                "data": None,
                "error": "No DataFrame in context"
            }

        df = context["df"]
        transformations = task.get("transformations", [])

        try:
            for transform in transformations:
                transform_type = transform.get("type")
                if transform_type == "drop_nulls":
                    columns = transform.get("columns")
                    df = df.dropna(subset=columns) if columns else df.dropna()
                elif transform_type == "fill_nulls":
                    df = df.fillna(transform.get("value", 0))
                elif transform_type == "convert_type":
                    column = transform.get("column")
                    dtype = transform.get("dtype")
                    df[column] = df[column].astype(dtype)
                elif transform_type == "rename":
                    df = df.rename(columns=transform.get("mapping", {}))

            return {
                "success": True,
                "data": df,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Transformation failed: {e}"
            }

    def _filter_data(self, task: Dict[str, Any], context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Filter data based on conditions"""
        if not context or "df" not in context:
            return {
                "success": False,
                "data": None,
                "error": "No DataFrame in context"
            }

        df = context["df"]

        try:
            filters = task.get("filters", {})
            start_date = filters.get("start_date")
            end_date = filters.get("end_date")
            region = filters.get("region")

            # Use existing filter function if applicable
            if any([start_date, end_date, region]):
                df = filter_data(df, start_date, end_date, region)

            # Apply custom filters
            custom_filters = filters.get("custom", [])
            for filt in custom_filters:
                column = filt.get("column")
                operator = filt.get("operator", "==")
                value = filt.get("value")

                if operator == "==":
                    df = df[df[column] == value]
                elif operator == ">":
                    df = df[df[column] > value]
                elif operator == "<":
                    df = df[df[column] < value]
                elif operator == "in":
                    df = df[df[column].isin(value)]

            return {
                "success": True,
                "data": df,
                "error": None,
                "metadata": {"filtered_rows": len(df)}
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Filtering failed: {e}"
            }

    def _save_data(self, task: Dict[str, Any], context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Save data to file"""
        if not context or "df" not in context:
            return {
                "success": False,
                "data": None,
                "error": "No DataFrame in context"
            }

        df = context["df"]
        output_path = task.get("output_path")

        try:
            if output_path.endswith('.csv'):
                df.to_csv(output_path, index=False)
            elif output_path.endswith('.parquet'):
                df.to_parquet(output_path, index=False)
            elif output_path.endswith(('.xlsx', '.xls')):
                df.to_excel(output_path, index=False)
            else:
                # Save both formats
                save_clean_data(df, output_path)

            return {
                "success": True,
                "data": None,
                "error": None,
                "metadata": {"output_path": output_path}
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"Save failed: {e}"
            }
