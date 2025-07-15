import streamlit as st
import pandas as pd
import os
import shutil
from datetime import datetime
from src.etl.load_superstore import load_and_clean_superstore, save_clean_data, filter_data
from src.utils.profiling import generate_profile

st.set_page_config(page_title="AutoPipelineAI", layout="wide")

st.title("🤖 AutoPipelineAI")
st.write("An LLM-Driven Agentic Framework for Autonomous ETL and DataOps")

# ──────────────────────────────────────────────
# 🔘 Interface Mode Selector
interface_mode = st.radio(
    "🔍 How would you like to proceed?",
    options=["", "Manual Mode: Filter + Dashboard", "LLM Mode: Smart Querying (Private LLM)"],
    horizontal=True
)

# ──────────────────────────────────────────────
# 🧰 Manual Mode: Reveal filter only when selected
if interface_mode == "Manual Mode: Filter + Dashboard":
    with st.expander("🔧 Manual ETL Controls (click to expand)", expanded=True):
        df = load_and_clean_superstore("input_docs/Sample - Superstore.csv")
        df['Order Date'] = pd.to_datetime(df['Order Date'])

        min_date = df['Order Date'].min().date()
        max_date = df['Order Date'].max().date()

        
        st.markdown(
    f"<h4>📅 Available Date Range in Data:</h4>"
    f"<p style='color:#00FFAA; font-size:18px;'><b>{min_date}</b> to <b>{max_date}</b></p>",
    unsafe_allow_html=True
                    )

        

        #st.markdown(f"### 📅 Available Date Range in Data: `{min_date}` to `{max_date}`")

        start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
        end_date = st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)

        region = st.selectbox("📍 Region Filter", options=["", "East", "West", "Central", "South"])

        query = st.text_input("🧠 Enter your ETL request (e.g., 'Extract sales from Q1 PDF')")

        if start_date > end_date:
            st.warning("⚠️ Start date must be before end date.")
            filtered_df = pd.DataFrame()  # empty
        else:
            # Default filtered data
            filtered_df = df[
                (df['Order Date'].dt.date >= start_date) &
                (df['Order Date'].dt.date <= end_date)
            ]
            if region:
                filtered_df = filtered_df[filtered_df["Region"] == region]

            st.dataframe(filtered_df)

        if query:
            if "superstore" in query.lower():
                df = load_and_clean_superstore("input_docs/Sample - Superstore.csv")
                df = filter_data(df,
                                 start_date=start_date if start_date else None,
                                 end_date=end_date if end_date else None,
                                 region=region if region else None)
                save_clean_data(df, "data/processed/superstore_cleaned")
                generate_profile(df)
                st.success("✅ Superstore data loaded, cleaned & profiled.")
                st.dataframe(df.head())

# ──────────────────────────────────────────────
# 🤖 LLM Mode: Only visible if selected
# 🤖 LLM Mode: Only visible if selected
elif interface_mode == "LLM Mode: Smart Querying (Private LLM)":
    with st.expander("🧠 LLM-Powered Smart Querying", expanded=True):
        import openai
        import json

        # Set up OpenAI API for Ollama
        openai.api_base = "http://localhost:11434/v1"
        openai.api_key = "ollama"

        st.markdown("## 🤖 Ask Questions About Your Data")

        # ✅ File Upload Block Starts Here
        st.markdown("---")
        st.subheader("📂 Upload Your Data")
        uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

        if uploaded_file is not None:
            file_name = uploaded_file.name
            save_path = os.path.join("input_docs", file_name)

            # Save or overwrite
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ File '{file_name}' saved to input_docs/")

            # Preview the uploaded file
            try:
                if file_name.endswith(".csv"):
                    try:
                        df = pd.read_csv(save_path, encoding="utf-8")
                    except UnicodeDecodeError:
                        df = pd.read_csv(save_path, encoding="latin1")  # fallback for Excel-exported CSVs
                elif file_name.endswith(".xlsx"):
                    df = pd.read_excel(save_path)

                st.dataframe(df.head(10), use_container_width=True)
                st.session_state["user_uploaded_df"] = df
            except Exception as e:
                st.error(f"❌ Error reading file: {e}")
        # ✅ File Upload Block Ends Here

        # 🧠 Natural Language Input for Questions
        # 🔀 Model Selector (llama3, mistral, phi3)
        st.markdown("---")
        st.subheader("🧠 Select Local LLM Model")
        llm_model = st.selectbox("Choose a local model", options=["llama3", "mistral","phi3"], index=0)

        # 🧠 Natural Language Input for Questions
        st.markdown("""
        Type a natural language question below.  
        **Example:**
        - *Top 10 products by sales in California in 2020*
        - *Show total profit by region between Jan 2020 and Jun 2020*
        """)
        user_query = st.text_input("🔎 Ask your question:", placeholder="e.g., What are the top 5 profitable categories in 2016?")

        if st.button("💡 Generate Insight") and user_query:
            if "user_uploaded_df" in st.session_state:
                df = st.session_state["user_uploaded_df"]
                df_sample_csv = df.head(10).to_csv(index=False)
                column_names = ", ".join(df.columns)

                prompt = f"""
                            You are a helpful data assistant. Analyze the following tabular data and answer the user's question.

                            Available columns in the dataset:
                            {column_names}

                            Use the DataFrame `df` already loaded in memory. Do NOT use `pd.read_csv`.

                            Here are the first 10 rows of the dataset (CSV format):
                            {df_sample_csv}

                            User's Question:
                            {user_query}

                            Give your answer in markdown format. If writing Python code, store the final result in a variable named `result`.
                        """

                with st.spinner("🤖 Thinking with LLM..."):
                    try:
                        import openai
                        openai.api_base = "http://localhost:11434/v1"
                        openai.api_key = "ollama"

                        client = openai.OpenAI(
                            base_url="http://localhost:11434/v1",
                            api_key="ollama"
                        )

                        response = client.chat.completions.create(
                            model=llm_model,
                            messages=[
                                {"role": "system", "content": "You are a helpful data analyst. Respond with brief insight and Python code (pandas only)."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.4,
                            stream=False
                        )

                        full_output = response.choices[0].message.content
                        st.markdown("### 🧠 LLM Insight")
                        st.markdown(full_output)

                        # ✅ Try extracting the code block from markdown
                        import re
                        match = re.search(r"```python(.*?)```", full_output, re.DOTALL)
                        if match:
                            code_str = match.group(1).strip()
                            st.markdown("### ⚙️ Executed Output")
                            try:
                                local_vars = {"df": df}
                                exec(code_str, {}, local_vars)
                                result = local_vars.get("result")  # expect result stored in variable `result`
                                if result is not None:
                                    st.dataframe(result)
                                else:
                                    st.warning("✅ Code executed, but no 'result' variable was found.")
                            except Exception as ex:
                                st.error(f"❌ Error running code: {ex}")
                        else:
                            st.warning("⚠️ No valid Python code block was found in the response.")

                    except Exception as e:
                        st.error(f"❌ LLM Error: {e}")
            else:
                st.warning("📂 Please upload a dataset first.")


        
