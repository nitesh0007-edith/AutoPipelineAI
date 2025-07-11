# 🤖 AutoPipelineAI

**LLM-Driven Agentic Framework for Autonomous ETL and DataOps**  
Designed and built by [Nitesh Ranjan Singh](https://github.com/nitesh0007-edith)

---

## 🚀 Project Summary

**AutoPipelineAI** is a next-generation open-source framework combining **LLMs**, **autonomous agents**, and **modular ETL pipelines** to automate complex data workflows from ingestion to analysis — all running **locally** on your machine.

> 🧠 Ask questions. Upload files. Get data cleaned, analyzed, and summarized — autonomously.

### 🔑 Key Features

- 💬 **LLM-powered natural language querying** over CSV, PDF, and logs
- 🔄 **Agent-based orchestration** using LangChain / CrewAI
- 🧼 **Autonomous ETL and data transformation**
- 🧪 **Schema validation + auto-profiling** using `ydata-profiling`
- 📊 **Interactive Streamlit dashboard** for upload, filtering, and insights
- 🧱 Fully extensible Python codebase with **no cloud dependency**

---

## 🧠 Why This Project Stands Out

| 🚀 Capability | ✅ Description |
|--------------|----------------|
| **Local LLM Integration** | Plug in **Ollama** for private LLM usage (no API key needed) |
| **Agentic Workflow** | Modular agents route tasks across ETL, profiling, QA |
| **Smart Prompt Engine** | Dynamic context-aware prompt creation from datasets |
| **Multimodal Ingestion** | Handle CSV, PDFs, and system logs seamlessly |
| **DataOps Friendly** | Built-in profiling, logging, and schema sanity checks |

---

## 🧱 Architecture Overview

```mermaid
graph TD;
    User["User Query or Upload (via Streamlit)"] --> Agent["LangChain/CrewAI Agent"];
    Agent -->|Task Decided| Router["ETL | Profiling | QA | NER | Query"];
    Router --> ETL[ETL Processor];
    Router --> Profiler[Profiling + Schema Validator];
    Router --> QA["PDF/Log/NLP Processor"];
    Router --> DBLayer["SQLite/DuckDB (planned)"];
    ETL --> Output["Cleaned/Queried Data"];
    QA --> Output;
    Profiler --> Output;

## 🗂️ Phase-Wise Progress

### ✅ Phase 1: Initialization
- Project bootstrapped with virtual environment and modular folders  
- Basic CLI + Streamlit setup for interaction

### ✅ Phase 2A: ETL & UI Foundations
- Ingested `Sample - Superstore.csv`  
- ETL module added for basic cleaning and transformation  
- Streamlit UI to upload data and apply filters

### ✅ Phase 2B: DataOps Capabilities
- Auto-profiling using `ydata-profiling`  
- Schema validation before transformation  
- Date & Region filters in Streamlit  
- Logging via `loguru`

### 🔄 Phase 3A: LLM Smart Querying (In Progress)
- User types questions like:  
  - "Show me top 5 categories by profit"  
  - "Which region underperformed in 2021?"
- LLM parses → Calls matching ETL/analysis functions → Returns structured result  
- Connected to local LLM via **Ollama**

### 🔜 Phase 3B: Autonomous Agents + Documents
- Multi-agent routing with **CrewAI**  
- PDF ingestion with NER extraction (PyMuPDF + spaCy)  
- SQLite / DuckDB for in-memory querying  
- Memory and caching layer for query optimization

---

## 📸 UI Snapshots

| Upload File | Auto Profile | Filtered Result |
|-------------|--------------|-----------------|
| *(coming soon)* | *(coming soon)* | *(coming soon)* |

---

## 🛠️ Tech Stack

| Tool/Library       | Purpose                           |
|--------------------|-----------------------------------|
| Python 3.10+       | Core logic                        |
| Streamlit          | UI & dashboard                    |
| Pandas             | DataFrame transformation          |
| ydata-profiling    | Automated EDA reports             |
| Loguru             | Logging & debugging               |
| LangChain / CrewAI | Agent orchestration (LLMs)        |
| Ollama             | Run local open-source LLMs        |
| PyMuPDF + spaCy    | (Upcoming) PDF parsing + NER      |
| SQLite / DuckDB    | (Planned) Query engine integration|

---

## 💻 How to Run Locally

```bash
# Clone the repo
git clone https://github.com/nitesh0007-edith/AutoPipelineAI.git
cd AutoPipelineAI

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Launch Streamlit app
streamlit run main.py

## 💬 Sample LLM Prompts (Planned)

- "Summarize total profit across all regions"  
- "Which segment had the highest returns in Q1?"  
- "List top 5 states by sales in Technology category"  
- "Extract key dates from uploaded invoice.pdf"

---

## 🧠 Upcoming Roadmap

- [ ] LLM-based dynamic ETL task generation  
- [ ] CrewAI for agent task delegation  
- [ ] Semantic search + Q&A from documents/logs  
- [ ] SQLite/DuckDB support  
- [ ] Auto-generated data pipeline documentation  
- [ ] Memory cache for repeated queries

---

## 👨‍💻 Author

**Nitesh Ranjan Singh**  
*Analyst (Data Engineer) @ IQVIA*  
*Incoming MSc Data Science (University of Glasgow)*

- 🌐 [GitHub](https://github.com/nitesh0007-edith)  
- 🔗 [LinkedIn](https://www.linkedin.com/in/nitesh0007/)

---

## 🙌 Contributions Welcome

If you're excited about autonomous data workflows, LLM agents, or local AI tools — feel free to fork, improve, or raise issues!

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).


