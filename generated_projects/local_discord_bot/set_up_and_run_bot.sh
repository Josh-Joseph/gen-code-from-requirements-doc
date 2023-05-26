#!/usr/bin/env bash

# Ensure the script is run from the correct directory
if [[ ! -f "requirements.txt" ]]; then
  echo "Please run this script from the project root directory."
  exit 1
fi

# Set up the virtual environment
echo "Setting up the virtual environment..."
python3 -m venv .venv

# Activate the virtual environment
echo "Activating the virtual environment..."
source .venv/bin/activate

# Install the required packages
echo "Installing required packages..."
pip install -r requirements.txt

# Run the tests
echo "Running tests..."
python -m unittest discover tests

# Check for the DISCORD_TOKEN environment variable
if [[ -z "${DISCORD_TOKEN}" ]]; then
  echo "Please set the DISCORD_TOKEN environment variable before running the bot."
  exit 1
fi

# Start the bot
echo "Starting the bot..."
python -m src.bot
