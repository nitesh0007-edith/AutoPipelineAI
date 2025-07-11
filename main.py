import streamlit as st
from src.etl.load_superstore import load_and_clean_superstore, save_clean_data, filter_data
from src.utils.profiling import generate_profile


st.set_page_config(page_title="AutoPipelineAI", layout="wide")

st.title("🤖 AutoPipelineAI")
st.write("An LLM-Driven Agentic Framework for Autonomous ETL and DataOps")

start_date = st.date_input("Start Date", value=None)
end_date = st.date_input("End Date", value=None)
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
