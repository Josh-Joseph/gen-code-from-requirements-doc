#!/bin/bash

# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run the main script
python src/main.py

# Deactivate the virtual environment
deactivate
