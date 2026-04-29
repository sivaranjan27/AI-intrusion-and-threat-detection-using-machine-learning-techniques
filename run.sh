#!/bin/bash

# Security Attack Detection System - Streamlit Launcher

echo "Security Attack Detection System"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher from https://www.python.org"
    exit 1
fi

echo "Python version:"
python3 --version
echo ""

# Check if requirements are installed
echo "Checking dependencies..."
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "Dependencies already installed"
fi

echo ""
echo "Starting Streamlit application..."
echo "The app will open at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run Streamlit
python3 -m streamlit run app.py
