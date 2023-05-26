#!/bin/bash

# Exit on error
set -e

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Run tests
python -m unittest discover tests

# Start the bot
python -m src.bot

# Deactivate virtual environment
deactivate
