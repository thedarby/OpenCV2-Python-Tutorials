#!/bin/bash
# Quick Start Script for Simple AI CLI

echo "=== Simple AI CLI - Quick Install ==="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3 first: https://www.python.org/downloads/"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Create virtual environment (optional but recommended)
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✓ Installation complete!"
echo ""
echo "=== Next Steps ==="
echo ""
echo "1. Run the setup wizard:"
echo "   python main.py setup"
echo ""
echo "2. Start chatting:"
echo "   python main.py chat \"Hello!\""
echo ""
echo "3. (Optional) Create an alias for easier access:"
echo "   echo 'alias ai=\"$(pwd)/run.sh\"' >> ~/.bashrc"
echo "   source ~/.bashrc"
echo "   ai chat \"Hello!\""
echo ""
