#!/bin/bash

# RAG AI Teaching Assistant - Setup Script
# This script helps set up the project for local development

echo "🎓 RAG AI Teaching Assistant - Setup"
echo "===================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Check for embeddings file
echo ""
if [ -f "embeddings.joblib" ]; then
    echo "✅ Found embeddings.joblib"
else
    echo "⚠️  Warning: embeddings.joblib not found"
    echo "   You'll need to run the preprocessing pipeline to generate it."
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file from template..."
    cp config.env.example .env
    echo "✅ Created .env file"
    echo "   Please edit .env with your configuration"
else
    echo ""
    echo "✅ .env file already exists"
fi

echo ""
echo "===================================="
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys or Ollama configuration"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run the app: streamlit run app.py"
echo ""

