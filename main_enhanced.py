"""
AutoPipelineAI - Enhanced Main Application
LLM-Driven Agentic Framework for Autonomous ETL and DataOps
"""
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from loguru import logger

# Import core modules
from src.etl.load_superstore import load_and_clean_superstore, save_clean_data, filter_data
from src.utils.profiling import generate_profile
from src.llm.ollama_client import OllamaClient
from src.llm.prompt_templates import PromptTemplates
from src.llm.code_executor import SafeCodeExecutor
from src.agents.orchestrator import AgentOrchestrator
from src.document.pdf_extractor import PDFExtractor
from src.document.ner_processor import NERProcessor
from src.database.duckdb_handler import DuckDBHandler
from src.cache.cache_manager import CacheManager
from src.cache.memory_store import MemoryStore

# Configure logging
logger.add("logs/app.log", rotation="1 MB", level="INFO")

# Page configuration
st.set_page_config(
    page_title="AutoPipelineAI - Enhanced",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "memory_store" not in st.session_state:
    st.session_state.memory_store = MemoryStore(max_history=50)

if "cache_manager" not in st.session_state:
    st.session_state.cache_manager = CacheManager(ttl_seconds=3600)

if "ollama_client" not in st.session_state:
    st.session_state.ollama_client = None

if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = None

# Sidebar
with st.sidebar:
    st.title("🤖 AutoPipelineAI")
    st.markdown("**Enhanced Version 0.3.0**")
    st.markdown("---")

    # Ollama Connection Status
    st.subheader("🔌 LLM Connection")

    if st.button("Check Ollama Status"):
        with st.spinner("Checking Ollama..."):
            try:
                client = OllamaClient()
                if client.check_connection():
                    st.success("✅ Ollama is running")
                    models = client.list_models()
                    if models:
                        st.info(f"📦 Available models: {', '.join(models)}")
                        st.session_state.ollama_client = client
                        st.session_state.orchestrator = AgentOrchestrator(client)
                    else:
                        st.warning("No models found. Please pull a model first.")
                else:
                    st.error("❌ Cannot connect to Ollama")
                    st.info("Start Ollama with: `ollama serve`")
            except Exception as e:
                st.error(f"Error: {e}")
                logger.error(f"Ollama connection error: {e}")

    st.markdown("---")

    # System Statistics
    st.subheader("📊 System Stats")

    memory_summary = st.session_state.memory_store.get_summary()
    st.metric("Conversations", memory_summary["conversation_messages"])

    cache_stats = st.session_state.cache_manager.get_stats()
    st.metric("Cache Entries", cache_stats["memory_entries"])

    if st.button("Clear All Cache"):
        st.session_state.cache_manager.clear("both")
        st.session_state.memory_store.clear_all()
        st.success("Cache cleared!")

    st.markdown("---")

    # Quick Actions
    st.subheader("⚡ Quick Actions")

    if st.button("Export Session"):
        export_path = f"data/exports/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs("data/exports", exist_ok=True)
        if st.session_state.memory_store.export_to_json(export_path):
            st.success(f"Exported to {export_path}")

# Main content
st.title("🤖 AutoPipelineAI")
st.markdown("**LLM-Driven Agentic Framework for Autonomous ETL and DataOps**")
st.markdown("---")

# Mode Selection
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Manual Mode",
    "🧠 LLM Mode",
    "🤝 Agent Mode",
    "📄 PDF Extraction",
    "🗄️ Database"
])

# ============================================
# TAB 1: Manual Mode
# ============================================
with tab1:
    st.header("📊 Manual Mode: Filter + Dashboard")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📂 Load Dataset")

        # File upload or use sample
        data_source = st.radio("Data Source", ["Sample Superstore", "Upload File"])

        df = None

        if data_source == "Sample Superstore":
            if st.button("Load Superstore Data"):
                with st.spinner("Loading..."):
                    try:
                        df = load_and_clean_superstore("input_docs/Sample - Superstore.csv")
                        st.session_state.memory_store.set_context("current_df", df)
                        st.success(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
                    except Exception as e:
                        st.error(f"Error loading data: {e}")
                        logger.error(f"Data loading error: {e}")

        else:
            uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx", "xls"])

            if uploaded_file:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)

                    st.session_state.memory_store.set_context("current_df", df)
                    st.success(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")

                except Exception as e:
                    st.error(f"Error reading file: {e}")

    with col2:
        st.subheader("⚙️ Actions")

        if st.session_state.memory_store.get_context("current_df") is not None:
            df = st.session_state.memory_store.get_context("current_df")

            if st.button("📊 Generate Profile Report"):
                with st.spinner("Generating profile..."):
                    try:
                        output_path = f"data/reports/profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                        generate_profile(df, output_path)
                        st.success(f"✅ Report saved to {output_path}")
                    except Exception as e:
                        st.error(f"Error generating profile: {e}")

            if st.button("💾 Save to Database"):
                with st.spinner("Saving to DuckDB..."):
                    try:
                        with DuckDBHandler("data/database.duckdb") as db:
                            db.create_table_from_df(df, "loaded_data")
                            st.success("✅ Saved to database")
                    except Exception as e:
                        st.error(f"Error saving to database: {e}")

    # Display data
    if st.session_state.memory_store.get_context("current_df") is not None:
        df = st.session_state.memory_store.get_context("current_df")

        st.subheader("📋 Data Preview")

        # Filters
        st.markdown("**Filters:**")

        filter_col1, filter_col2, filter_col3 = st.columns(3)

        with filter_col1:
            if "Order Date" in df.columns:
                df['Order Date'] = pd.to_datetime(df['Order Date'])
                min_date = df['Order Date'].min().date()
                max_date = df['Order Date'].max().date()

                start_date = st.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
                end_date = st.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

                if start_date <= end_date:
                    df = df[(df['Order Date'].dt.date >= start_date) & (df['Order Date'].dt.date <= end_date)]

        with filter_col2:
            if "Region" in df.columns:
                regions = ["All"] + sorted(df["Region"].unique().tolist())
                selected_region = st.selectbox("Region", regions)

                if selected_region != "All":
                    df = df[df["Region"] == selected_region]

        with filter_col3:
            st.metric("Filtered Rows", len(df))

        # Display dataframe
        st.dataframe(df, use_container_width=True, height=400)

        # Quick stats
        st.subheader("📈 Quick Statistics")

        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

        numeric_cols = df.select_dtypes(include=['number']).columns

        if len(numeric_cols) > 0:
            with stat_col1:
                st.metric("Total Rows", len(df))

            with stat_col2:
                st.metric("Columns", len(df.columns))

            with stat_col3:
                if "Sales" in df.columns:
                    st.metric("Total Sales", f"${df['Sales'].sum():,.2f}")

            with stat_col4:
                if "Profit" in df.columns:
                    st.metric("Total Profit", f"${df['Profit'].sum():,.2f}")

# ============================================
# TAB 2: LLM Mode
# ============================================
with tab2:
    st.header("🧠 LLM Mode: Smart Querying")

    if st.session_state.ollama_client is None:
        st.warning("⚠️ Please check Ollama connection in the sidebar first!")
    else:
        col1, col2 = st.columns([3, 1])

        with col1:
            st.subheader("💬 Ask Questions About Your Data")

            # Get available models
            models = st.session_state.ollama_client.list_models()

            if not models:
                st.error("No models available. Please pull a model: `ollama pull llama3`")
            else:
                selected_model = st.selectbox("Select Model", models)

                user_query = st.text_area(
                    "Enter your question:",
                    placeholder="e.g., What are the top 10 products by sales in 2020?",
                    height=100
                )

                if st.button("🚀 Generate Answer", type="primary"):
                    if not user_query:
                        st.warning("Please enter a question")
                    elif st.session_state.memory_store.get_context("current_df") is None:
                        st.warning("Please load a dataset first (Manual Mode tab)")
                    else:
                        df = st.session_state.memory_store.get_context("current_df")

                        with st.spinner("🤖 Analyzing with LLM..."):
                            try:
                                # Generate prompt
                                prompt = PromptTemplates.data_analysis_prompt(df, user_query)

                                # Get LLM response
                                llm_response = st.session_state.ollama_client.generate_completion(
                                    prompt=prompt,
                                    model=selected_model,
                                    temperature=0.4
                                )

                                # Display response
                                st.markdown("### 💡 LLM Response")
                                st.markdown(llm_response)

                                # Execute code
                                executor = SafeCodeExecutor()
                                result = executor.execute_from_llm_response(
                                    llm_response,
                                    context={"df": df, "pd": pd}
                                )

                                if result["success"]:
                                    st.markdown("### ✅ Execution Result")

                                    if isinstance(result["result"], pd.DataFrame):
                                        st.dataframe(result["result"], use_container_width=True)
                                    elif isinstance(result["result"], (list, tuple, dict)):
                                        st.json(result["result"])
                                    elif result["result"] is not None:
                                        st.success(f"Result: {result['result']}")

                                    if result["output"]:
                                        st.text("Output:\n" + result["output"])

                                    # Log to memory
                                    st.session_state.memory_store.add_message("user", user_query)
                                    st.session_state.memory_store.add_message("assistant", llm_response)

                                else:
                                    st.error(f"Execution failed: {result['error']}")

                            except Exception as e:
                                st.error(f"Error: {e}")
                                logger.error(f"LLM query error: {e}")

        with col2:
            st.subheader("📜 History")

            history = st.session_state.memory_store.get_conversation_history(limit=5)

            if history:
                for msg in reversed(history):
                    role_icon = "👤" if msg["role"] == "user" else "🤖"
                    with st.expander(f"{role_icon} {msg['role'].title()}", expanded=False):
                        st.text(msg["content"][:200] + "..." if len(msg["content"]) > 200 else msg["content"])
            else:
                st.info("No conversation history yet")

# ============================================
# TAB 3: Agent Mode
# ============================================
with tab3:
    st.header("🤝 Agent Mode: Multi-Agent Orchestration")

    if st.session_state.orchestrator is None:
        st.warning("⚠️ Please check Ollama connection in the sidebar first!")
    else:
        st.markdown("Let multiple specialized agents handle your workflow automatically.")

        # Natural language workflow
        st.subheader("📝 Describe Your Workflow")

        workflow_description = st.text_area(
            "Describe what you want to do:",
            placeholder="e.g., Load the superstore data, filter it for 2020, calculate total sales by region, and generate a profile report",
            height=100
        )

        if st.button("🎯 Execute Workflow", type="primary"):
            if not workflow_description:
                st.warning("Please describe your workflow")
            else:
                with st.spinner("🤖 Planning and executing workflow..."):
                    try:
                        orchestrator = st.session_state.orchestrator

                        # Parse workflow
                        tasks = orchestrator.parse_natural_language_workflow(workflow_description)

                        st.info(f"📋 Planned {len(tasks)} tasks")

                        # Display tasks
                        for i, task in enumerate(tasks, 1):
                            st.markdown(f"**Task {i}:** {task.get('type')} - {task.get('description', 'N/A')}")

                        # Execute workflow
                        results = orchestrator.execute_workflow(tasks)

                        # Display results
                        st.markdown("---")
                        st.subheader("📊 Results")

                        for i, result in enumerate(results, 1):
                            status_icon = "✅" if result["success"] else "❌"

                            with st.expander(f"{status_icon} Task {i} - {'Success' if result['success'] else 'Failed'}"):
                                if result["success"]:
                                    if isinstance(result.get("data"), pd.DataFrame):
                                        st.dataframe(result["data"].head())
                                    elif result.get("data"):
                                        st.json(result.get("data"))

                                    if result.get("metadata"):
                                        st.json(result["metadata"])
                                else:
                                    st.error(result.get("error", "Unknown error"))

                        # Show agent stats
                        st.markdown("---")
                        st.subheader("🤖 Agent Statistics")

                        agent_stats = orchestrator.get_agent_stats()

                        stats_df = pd.DataFrame(agent_stats)
                        st.dataframe(stats_df, use_container_width=True)

                    except Exception as e:
                        st.error(f"Workflow execution failed: {e}")
                        logger.error(f"Workflow error: {e}")

# ============================================
# TAB 4: PDF Extraction
# ============================================
with tab4:
    st.header("📄 PDF Extraction & NER")

    st.subheader("📤 Upload PDF")

    uploaded_pdf = st.file_uploader("Upload PDF file", type=["pdf"])

    if uploaded_pdf:
        # Save uploaded file
        pdf_path = f"input_docs/{uploaded_pdf.name}"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_pdf.getbuffer())

        st.success(f"✅ Uploaded: {uploaded_pdf.name}")

        # Extraction options
        extraction_type = st.selectbox(
            "What do you want to extract?",
            ["Text", "Tables", "Metadata", "Everything", "Named Entities (NER)"]
        )

        if st.button("🔍 Extract"):
            with st.spinner(f"Extracting {extraction_type.lower()}..."):
                try:
                    extractor = PDFExtractor()

                    if extraction_type == "Text":
                        text = extractor.extract_text(pdf_path)
                        st.text_area("Extracted Text", text, height=400)

                    elif extraction_type == "Tables":
                        tables = extractor.extract_tables(pdf_path)

                        if tables:
                            st.success(f"✅ Found {len(tables)} tables")

                            for i, table_df in enumerate(tables, 1):
                                st.markdown(f"**Table {i}** (Page {table_df.attrs.get('page', 'N/A')})")
                                st.dataframe(table_df, use_container_width=True)

                                # Option to save
                                if st.button(f"Save Table {i}", key=f"save_table_{i}"):
                                    output_path = f"data/extracted/table_{i}.csv"
                                    os.makedirs("data/extracted", exist_ok=True)
                                    table_df.to_csv(output_path, index=False)
                                    st.success(f"Saved to {output_path}")
                        else:
                            st.warning("No tables found")

                    elif extraction_type == "Metadata":
                        metadata = extractor.extract_metadata(pdf_path)
                        st.json(metadata)

                    elif extraction_type == "Everything":
                        data = extractor.extract_all(pdf_path)

                        st.markdown("### 📋 Metadata")
                        st.json(data["metadata"])

                        st.markdown("### 📝 Text")
                        st.text_area("Text", data["text"], height=200)

                        st.markdown("### 📊 Tables")
                        if data["tables"]:
                            for i, table_df in enumerate(data["tables"], 1):
                                with st.expander(f"Table {i}"):
                                    st.dataframe(table_df)
                        else:
                            st.info("No tables found")

                    elif extraction_type == "Named Entities (NER)":
                        text = extractor.extract_text(pdf_path)
                        ner = NERProcessor(use_spacy=True)
                        entities = ner.extract_structured_data(text)

                        st.markdown("### 🏷️ Extracted Entities")
                        st.json(entities["entities"])

                        st.markdown("### 📊 Metadata")
                        st.json(entities["metadata"])

                except Exception as e:
                    st.error(f"Extraction failed: {e}")
                    logger.error(f"PDF extraction error: {e}")

# ============================================
# TAB 5: Database
# ============================================
with tab5:
    st.header("🗄️ Database Management")

    db_type = st.selectbox("Database Type", ["DuckDB", "SQLite"])

    if db_type == "DuckDB":
        st.subheader("🦆 DuckDB Interface")

        with DuckDBHandler("data/database.duckdb") as db:
            # List tables
            tables = db.list_tables()

            if tables:
                st.markdown(f"**Available Tables:** {', '.join(tables)}")

                selected_table = st.selectbox("Select Table", tables)

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("View Schema"):
                        schema = db.get_table_schema(selected_table)
                        st.dataframe(schema)

                with col2:
                    if st.button("View Stats"):
                        stats = db.aggregate_stats(selected_table)
                        st.json(stats)

                # Query interface
                st.subheader("💻 SQL Query")

                query = st.text_area(
                    "Enter SQL query:",
                    value=f"SELECT * FROM {selected_table} LIMIT 10",
                    height=100
                )

                if st.button("▶️ Run Query"):
                    try:
                        result = db.query(query)
                        st.dataframe(result, use_container_width=True)
                        st.info(f"Returned {len(result)} rows")
                    except Exception as e:
                        st.error(f"Query error: {e}")

            else:
                st.info("No tables in database. Load data from Manual Mode tab.")

# Footer
st.markdown("---")
st.markdown("**AutoPipelineAI v0.3.0** | Built with ❤️ using Streamlit, LangChain, and Ollama")
