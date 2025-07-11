import streamlit as st
import pandas as pd
from datetime import datetime
from src.etl.load_superstore import load_and_clean_superstore, save_clean_data, filter_data
from src.utils.profiling import generate_profile


st.set_page_config(page_title="AutoPipelineAI", layout="wide")

st.title("🤖 AutoPipelineAI")
st.write("An LLM-Driven Agentic Framework for Autonomous ETL and DataOps")

df = load_and_clean_superstore("input_docs/Sample - Superstore.csv")

# Ensure 'Order Date' is datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Get min and max dates
min_date = df['Order Date'].min().date()
max_date = df['Order Date'].max().date()

# Show min/max info on dashboard
st.markdown(f"### 📅 Available Date Range in Data: `{min_date}` to `{max_date}`")

# Date filter inputs restricted within min/max
start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
end_date = st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)

# Filter data accordingly
if start_date > end_date:
    st.warning("⚠️ Start date must be before end date.")
    filtered_df = pd.DataFrame()  # empty
else:
    filtered_df = df[(df['Order Date'].dt.date >= start_date) & (df['Order Date'].dt.date <= end_date)]
region = st.selectbox("Region", options=["", "East", "West", "Central", "South"])

query = st.text_input("🧠 Enter your ETL request (e.g., 'Extract sales from Q1 PDF')")

if query:
    if "superstore" in query.lower():
        df = load_and_clean_superstore("input_docs/Sample - Superstore.csv")
        df = filter_data(df, start_date=start_date if start_date else None,
                     end_date=end_date if end_date else None,
                     region=region if region else None)
        save_clean_data(df, "data/processed/superstore_cleaned")
        generate_profile(df)
        st.success("✅ Superstore data loaded, cleaned & profiled.")
        st.dataframe(df.head())
