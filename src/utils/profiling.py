from ydata_profiling import ProfileReport
import pandas as pd
import os

def generate_profile(df: pd.DataFrame, output_path: str = "data/reports/superstore_profile.html"):
    """
    Generate and save a profiling report as an HTML file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    profile = ProfileReport(df, title="Superstore Data Report", explorative=True)
    profile.to_file(output_file=output_path)