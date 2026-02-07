#!/bin/bash
# CosmicStudio Quick Start Script

echo "=================================="
echo "  CosmicStudio Quick Start"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "Installation complete!"
echo ""
echo "Starting CosmicStudio..."
echo ""

# Run the application
cd src
python main.py

# Deactivate on exit
deactivate
