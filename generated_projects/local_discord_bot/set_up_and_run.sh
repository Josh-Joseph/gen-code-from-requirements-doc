#!/usr/bin/env bash

# Create and activate virtual environment
echo "Creating and activating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Run tests
echo "Running tests..."
python -m unittest discover tests

# Start the bot
echo "Starting the bot..."
python src/bot.py
