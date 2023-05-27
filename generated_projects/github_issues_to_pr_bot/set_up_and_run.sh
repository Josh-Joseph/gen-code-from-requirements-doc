#!/bin/bash

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run tests
# python -m unittest discover tests

# Start the bot
python src/bot.py

# Deactivate virtual environment
deactivate
