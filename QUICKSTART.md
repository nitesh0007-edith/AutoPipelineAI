# 🚀 QuickStart Guide - AutoPipelineAI v0.3.0

Get up and running with AutoPipelineAI in 5 minutes!

## ⚡ Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/nitesh0007-edith/AutoPipelineAI.git
cd AutoPipelineAI

# Run automated setup
chmod +x setup.sh
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Run the enhanced version
streamlit run main_enhanced.py
```

## 📋 Manual Setup

### 1. Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

### 2. Installation

```bash
# Clone repository
git clone https://github.com/nitesh0007-edith/AutoPipelineAI.git
cd AutoPipelineAI

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir -p data/{cache,database,processed,reports,exports,extracted}
mkdir -p logs input_docs

# Copy environment template
cp .env.template .env
```

### 3. Optional: Setup Ollama (For LLM Features)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama (in a separate terminal)
ollama serve

# Pull models
ollama pull llama3
ollama pull mistral
ollama pull phi3
```

### 4. Optional: Install spaCy Model (For NER)

```bash
python -m spacy download en_core_web_sm
```

## 🎮 First Run

### Option 1: Enhanced Version (Recommended)

```bash
streamlit run main_enhanced.py
```

This includes all features:
- ✅ Manual Mode
- ✅ LLM Mode
- ✅ Agent Mode
- ✅ PDF Extraction
- ✅ Database Interface

### Option 2: Original Version

```bash
streamlit run main.py
```

This includes basic features:
- ✅ Manual Mode
- ✅ LLM Mode

## 📊 Quick Test

Once the app is running:

1. **Test Manual Mode:**
   - Click "Load Superstore Data"
   - Explore the dashboard
   - Generate a profile report

2. **Test LLM Mode** (requires Ollama):
   - Check Ollama connection in sidebar
   - Load sample data
   - Ask: "What are the top 5 products by sales?"

3. **Test Agent Mode** (requires Ollama):
   - Describe a workflow: "Load data, filter for 2020, and create a report"
   - Watch agents work automatically

## 🔧 Troubleshooting

### Ollama Not Connecting

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve

# Verify models are installed
ollama list
```

### Import Errors

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### spaCy Model Missing

```bash
# Download the model
python -m spacy download en_core_web_sm
```

### Permission Issues

```bash
# Fix directory permissions
chmod -R 755 data logs
```

## 📚 Next Steps

1. **Read the full README:** [README_v0.3.md](README_v0.3.md)
2. **Explore the modes:** Try each of the 5 operational modes
3. **Run tests:** `pytest tests/ -v`
4. **Customize:** Edit `.env` file for your preferences
5. **Contribute:** Check out [CONTRIBUTING.md](CONTRIBUTING.md) (if available)

## 💡 Sample Workflows

### Data Analysis

```
Mode: LLM Mode
Query: "Show me the top 10 products by profit margin"
```

### PDF Processing

```
Mode: PDF Extraction
Action: Upload invoice → Extract tables → Save to database
```

### Automated Workflow

```
Mode: Agent Mode
Workflow: "Load sales data, calculate regional totals, and generate a comprehensive report"
```

## 🆘 Getting Help

- 📖 **Documentation:** [README_v0.3.md](README_v0.3.md)
- 🐛 **Issues:** [GitHub Issues](https://github.com/nitesh0007-edith/AutoPipelineAI/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/nitesh0007-edith/AutoPipelineAI/discussions)

## 🎯 Key Features to Try

1. **Natural Language Queries** - Ask questions in plain English
2. **Multi-Agent Workflows** - Let AI orchestrate complex tasks
3. **PDF Extraction** - Extract tables and entities from documents
4. **Database Analytics** - Run SQL queries on your data
5. **Auto-Profiling** - Get comprehensive data quality reports

---

**Ready to automate your data workflows? Let's go! 🚀**
