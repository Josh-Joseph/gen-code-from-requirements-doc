#!/usr/bin/env bash
set -e

# Check if TOKEN_FOR_GITHUB is set
if [ -z "$TOKEN_FOR_GITHUB" ]; then
  echo "Error: TOKEN_FOR_GITHUB environment variable is not set."
  exit 1
fi

# Create and activate virtual environment
echo "Creating and activating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install required packages
echo "Installing required packages..."
python3 -m pip install -r requirements.txt

# Run tests
echo "Running tests..."
python3 -m unittest discover tests

# Start the bot
echo "Starting the bot..."
python3 src/main.py
