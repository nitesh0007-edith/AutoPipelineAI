"""
Prompt Templates - Reusable prompt templates for different tasks
"""
from typing import Dict, List, Optional
import pandas as pd


class PromptTemplates:
    """Collection of prompt templates for various data tasks"""

    @staticmethod
    def data_analysis_prompt(
        df: pd.DataFrame,
        user_query: str,
        sample_rows: int = 10
    ) -> str:
        """
        Generate prompt for data analysis tasks

        Args:
            df: DataFrame to analyze
            user_query: User's question
            sample_rows: Number of sample rows to include

        Returns:
            Formatted prompt string
        """
        df_sample_csv = df.head(sample_rows).to_csv(index=False)
        column_info = "\n".join([f"- {col}: {dtype}" for col, dtype in df.dtypes.items()])

        return f"""You are a helpful data analyst assistant. Analyze the following dataset and answer the user's question.

Dataset Information:
- Total Rows: {len(df)}
- Total Columns: {len(df.columns)}

Column Details:
{column_info}

Sample Data (first {sample_rows} rows):
```csv
{df_sample_csv}
```

IMPORTANT INSTRUCTIONS:
- Use the DataFrame `df` already loaded in memory. DO NOT use pd.read_csv() or load data.
- Write Python code using pandas to answer the question.
- Store the final result in a variable named `result`.
- Keep code concise and efficient.
- If visualization is needed, use plotly or matplotlib.

User's Question:
{user_query}

Provide your answer in the following format:
1. Brief explanation of your approach
2. Python code in a ```python``` code block
3. Expected output description
"""

    @staticmethod
    def etl_task_prompt(
        task_description: str,
        available_files: List[str],
        output_format: str = "CSV"
    ) -> str:
        """
        Generate prompt for ETL task planning

        Args:
            task_description: Description of ETL task
            available_files: List of available data files
            output_format: Desired output format

        Returns:
            Formatted prompt string
        """
        files_list = "\n".join([f"- {file}" for file in available_files])

        return f"""You are an ETL specialist. Plan and execute the following data transformation task.

Available Data Files:
{files_list}

Task Description:
{task_description}

Output Format: {output_format}

Provide a step-by-step plan with Python code to:
1. Load the necessary data
2. Transform/clean the data
3. Save to {output_format} format

Format your response with:
- Clear step descriptions
- Python code in ```python``` blocks
- Error handling considerations
"""

    @staticmethod
    def sql_generation_prompt(
        table_schema: Dict[str, str],
        natural_query: str,
        dialect: str = "DuckDB"
    ) -> str:
        """
        Generate prompt for SQL query generation

        Args:
            table_schema: Dictionary of table name to schema
            natural_query: Natural language query
            dialect: SQL dialect (DuckDB, SQLite, etc.)

        Returns:
            Formatted prompt string
        """
        schema_text = ""
        for table, schema in table_schema.items():
            schema_text += f"\nTable: {table}\n{schema}\n"

        return f"""You are a SQL expert. Convert the following natural language query to {dialect} SQL.

Database Schema:
{schema_text}

Natural Language Query:
{natural_query}

Provide:
1. The SQL query in a ```sql``` code block
2. Brief explanation of what the query does
3. Any assumptions made

SQL Dialect: {dialect}
"""

    @staticmethod
    def data_quality_prompt(df: pd.DataFrame) -> str:
        """
        Generate prompt for data quality assessment

        Args:
            df: DataFrame to assess

        Returns:
            Formatted prompt string
        """
        null_counts = df.isnull().sum()
        null_info = "\n".join([f"- {col}: {count} nulls ({count/len(df)*100:.1f}%)"
                               for col, count in null_counts.items() if count > 0])

        return f"""Analyze the data quality of this dataset and provide recommendations.

Dataset Information:
- Total Rows: {len(df)}
- Total Columns: {len(df.columns)}
- Columns: {', '.join(df.columns)}

Null Values:
{null_info if null_info else "- No null values found"}

Data Types:
{df.dtypes.to_string()}

Please provide:
1. Data quality issues identified
2. Recommended cleaning steps
3. Python code to fix issues (in ```python``` blocks)
4. Validation checks to ensure quality
"""

    @staticmethod
    def pdf_extraction_prompt(pdf_path: str, extraction_type: str = "tables") -> str:
        """
        Generate prompt for PDF extraction guidance

        Args:
            pdf_path: Path to PDF file
            extraction_type: Type of extraction (tables, text, forms)

        Returns:
            Formatted prompt string
        """
        return f"""Extract {extraction_type} from the following PDF file: {pdf_path}

Provide Python code using pdfplumber or PyMuPDF to:
1. Open and read the PDF
2. Extract {extraction_type}
3. Convert to structured format (DataFrame for tables, dict for forms, string for text)
4. Handle errors gracefully

Include the code in a ```python``` block.
"""

    @staticmethod
    def agent_routing_prompt(user_request: str, available_agents: List[str]) -> str:
        """
        Generate prompt for routing requests to appropriate agent

        Args:
            user_request: User's request
            available_agents: List of available agent types

        Returns:
            Formatted prompt string
        """
        agents_list = "\n".join([f"- {agent}" for agent in available_agents])

        return f"""You are a task router. Analyze the user request and determine which agent should handle it.

Available Agents:
{agents_list}

User Request:
{user_request}

Respond with ONLY a valid JSON object in this format:
{{
    "selected_agent": "agent_name",
    "reasoning": "brief explanation",
    "task_breakdown": ["step1", "step2", "step3"]
}}
"""
