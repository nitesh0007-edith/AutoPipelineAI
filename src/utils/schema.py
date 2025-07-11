import pandas as pd

def validate_schema(df: pd.DataFrame, expected_columns: list) -> bool:
    """
    Check if the required columns exist in the dataframe.
    """
    missing = [col for col in expected_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return True