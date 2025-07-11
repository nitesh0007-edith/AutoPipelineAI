import pandas as pd
import os
from loguru import logger
from datetime import datetime
from src.utils.schema import validate_schema

# Logging setup
logger.add("logs/etl_superstore.log", rotation="500 KB")

def load_and_clean_superstore(csv_path: str) -> pd.DataFrame:
    """
    Load and clean the Superstore dataset.
    """
    logger.info(f"Loading file from {csv_path}")
    
    try:
        df = pd.read_csv(csv_path, encoding='ISO-8859-1')
    except Exception as e:
        logger.error(f"Failed to read CSV: {e}")
        raise
    
    required_cols = [
    "Order Date", "Ship Date", "Sales", "Profit", "Region", "Category", "Sub-Category"]
    validate_schema(df, required_cols)

    # Convert dates
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors='coerce')
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors='coerce')

    # Strip whitespace from string columns
    str_cols = df.select_dtypes(include=['object']).columns
    df[str_cols] = df[str_cols].apply(lambda x: x.str.strip())

    # Drop rows with missing essential values
    df.dropna(subset=["Order ID", "Sales", "Profit"], inplace=True)

    logger.info(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns")

    return df

def save_clean_data(df: pd.DataFrame, out_path: str):
    """
    Save cleaned DataFrame to CSV and Parquet formats.
    """
    logger.info(f"Saving cleaned data to {out_path}")
    
    df.to_csv(f"{out_path}.csv", index=False)
    df.to_parquet(f"{out_path}.parquet", index=False)

    logger.success("Cleaned data saved successfully.")

def filter_data(df: pd.DataFrame, start_date=None, end_date=None, region=None):
    """
    Filter data by date range and region.
    """
    if start_date:
        df = df[df["Order Date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["Order Date"] <= pd.to_datetime(end_date)]
    if region:
        df = df[df["Region"].str.lower() == region.lower()]
    return df

