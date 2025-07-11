# 🤖 AutoPipelineAI

**An LLM-Driven Agentic Framework for Autonomous ETL and DataOps**  
Designed and built by [Nitesh Ranjan Singh](https://github.com/nitesh0007-edith)

---

## 🚀 Project Summary

AutoPipelineAI is an open-source, end-to-end **LLM + Agentic AI powered data engineering framework** that automates ETL workflows, performs intelligent data operations, and enables natural language querying over structured and unstructured data. It integrates:

- 🧠 **LLMs (GPT/Mistral)** for understanding business context
- 🔗 **LangChain / CrewAI / LangGraph** for agentic decision-making
- 🧼 **Automated ETL Pipelines** using Python + Pandas
- 📊 **Streamlit dashboards** for user interaction
- 📄 **Multimodal data ingestion** (CSV, PDF, logs)
- ✅ **Schema validation + profiling** for DataOps
- 🔁 Fully extensible + runs locally (no cloud dependency)

---

## 🧱 Project Architecture

User Query → Streamlit UI
↓
LangChain Agent (LLM)
↓
Intelligently Routes To:

ETL Module (Extract + Transform)

Data Validation + Profiling

Semantic Search

Data Pipeline Generator
↓
Returns Cleaned, Filtered, or Queried Data


---

## 🗂️ Phases Overview

### ✅ Phase 1: Project Initialization

- 🏗️ Project folder structure set up with `venv`, `src/`, `data/`, and `main.py`
- 📦 Requirements listed for easy reproducibility
- 🔒 `.gitignore` created to exclude logs, virtualenv, cache, etc.

---

### ✅ Phase 2: ETL Foundation & Local Ingestion

- 📁 Ingested sample Superstore dataset (`input_docs/Sample - Superstore.csv`)
- 🧹 Cleaned data saved to `data/processed/`
- 🪵 Logging via `loguru`
- 📊 Streamlit interface for manual data triggers

---

### ✅ Phase 2B: Enhancements for DataOps

- 📈 **Automatic profiling** via `ydata-profiling`
  - Outputs interactive HTML reports (`data/reports/superstore_profile.html`)
- 📆 **Date & Region filtering** via Streamlit inputs
- 🔍 **Schema validator** to check column sanity before transformation

---

### 🔜 Phase 3: LLM + Agentic Pipeline (Upcoming)

- 🤖 LLM-enabled agent (using LangChain / CrewAI)
- 📌 User types queries like:
  - *“Show me sales trend in West for January 2021”*
  - *“What products drive profit in Furniture category?”*
- 📄 LLM parses → selects ETL functions → executes → returns answers
- 📘 PDF/Log Ingestion + NER for documents and audit logs

---

## 📸 UI Preview (Streamlit)

| Upload Data | Profiling | Filters |
|-------------|-----------|---------|
| ![upload](https://imgur.com/upload_sample.png) | ![profile](https://imgur.com/profile_sample.png) | ![filters](https://imgur.com/filters_sample.png) |

---

## 🛠️ Tech Stack

| Tool           | Purpose                                  |
|----------------|------------------------------------------|
| Python (3.10+) | Core logic + ETL                         |
| Streamlit      | UI + User interaction                    |
| Pandas         | DataFrame operations                     |
| Loguru         | Smart logging                            |
| ydata-profiling| Auto EDA profiling                       |
| LangChain / CrewAI | LLM & agentic decision-making      |

---

## 🧪 Local Setup

```bash
git clone https://github.com/nitesh0007-edith/AutoPipelineAI.git
cd AutoPipelineAI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run main.py

🧠 Upcoming Features
LLM-based dynamic ETL generation

CrewAI/LangGraph-based task routing

Document/question answering from PDFs, logs, dashboards

Integration with SQLite or DuckDB for query layer

👨‍💻 Author
Nitesh Ranjan Singh

Analyst (Data Engineer) @ IQVIA | MSc Data Science (University of Glasgow)

---

## ✅ To Use