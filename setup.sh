#!/bin/bash

# AutoPipelineAI Setup Script
# This script sets up the AutoPipelineAI environment

set -e

echo "🤖 AutoPipelineAI v0.3.0 Setup"
echo "================================"
echo ""

# Check Python version
echo "📌 Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python 3.10 or higher is required. Current version: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python version: $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate || . venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip
echo "✅ pip upgraded"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p data/cache
mkdir -p data/database
mkdir -p data/processed
mkdir -p data/reports
mkdir -p data/exports
mkdir -p data/extracted
mkdir -p data/extracted_images
mkdir -p input_docs
mkdir -p logs
echo "✅ Directories created"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.template .env
    echo "✅ .env file created"
else
    echo "ℹ️  .env file already exists, skipping..."
fi
echo ""

# Download spaCy model
echo "📥 Downloading spaCy model for NER..."
python -m spacy download en_core_web_sm || echo "⚠️  spaCy model download failed (optional feature)"
echo ""

# Check if Ollama is installed
echo "🔍 Checking for Ollama installation..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is installed"
    echo "ℹ️  To use LLM features, run: ollama serve"
    echo "ℹ️  Then pull models: ollama pull llama3"
else
    echo "⚠️  Ollama not found. Install from: https://ollama.ai"
    echo "ℹ️  Ollama is required for LLM features"
fi
echo ""

# Run tests
echo "🧪 Running tests..."
pytest tests/ -v || echo "⚠️  Some tests failed (optional)"
echo ""

echo "================================"
echo "🎉 Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. (Optional) Install Ollama from: https://ollama.ai"
echo "3. (Optional) Pull LLM model: ollama pull llama3"
echo "4. Run the app:"
echo "   - Original: streamlit run main.py"
echo "   - Enhanced: streamlit run main_enhanced.py"
echo ""
echo "Happy analyzing! 🚀"
