#!/bin/bash
echo "==========================================="
echo "Setting up Trail Camera Photo Scanner..."
echo "==========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 could not be found."
    echo "Please install Python 3 and try again."
    exit 1
fi

echo "Creating virtual environment (venv)..."
python3 -m venv venv

echo ""
echo "Activating virtual environment and installing dependencies..."
echo "This may take a few minutes depending on your internet connection..."
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Downloading AI Model for offline use..."
python download_model.py

echo ""
echo "==========================================="
echo "Setup Complete!"
echo "==========================================="
echo ""
echo "To run the scanner in the future:"
echo "1. Open your terminal in this folder"
echo "2. Type: source venv/bin/activate"
echo "3. Type: python scanner.py"
echo ""
