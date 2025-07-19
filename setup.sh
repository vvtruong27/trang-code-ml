#!/bin/bash

echo "🚀 Setting up Email Classification API..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Setup completed successfully!"
echo ""
echo "🎯 Start the API server:"

source .venv/bin/activate
cd email_classification_module
python api_backend.py

echo ""
echo "🌐 API will be available at: http://localhost:5001"
echo "📚 Swagger UI: http://localhost:5001/swagger" 