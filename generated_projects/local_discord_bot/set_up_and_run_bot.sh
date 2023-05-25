#!/usr/bin/env bash
set -e

# Check for required commands
command -v python3 >/dev/null 2>&1 || { echo >&2 "python3 is required but not installed. Aborting."; exit 1; }
command -v pip >/dev/null 2>&1 || { echo >&2 "pip is required but not installed. Aborting."; exit 1; }
command -v pytest >/dev/null 2>&1 || { echo >&2 "pytest is required but not installed. Aborting."; exit 1; }

# Check for DISCORD_TOKEN environment variable
if [ -z "$DISCORD_TOKEN" ]; then
  echo "Error: DISCORD_TOKEN environment variable is not set. Please set it before running the script."
  exit 1
fi

# Set up the virtual environment
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
else
  echo "Virtual environment already exists. Skipping creation."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install the required packages
if [ -f "requirements.txt" ]; then
  echo "Installing required packages..."
  pip install -r requirements.txt
else
  echo "Error: requirements.txt not found. Aborting."
  exit 1
fi

# Run the tests
if [ -d "tests" ]; then
  echo "Running tests..."
  pytest tests/
else
  echo "Error: tests directory not found. Aborting."
  exit 1
fi

# Start the bot
if [ -f "src/bot.py" ]; then
  echo "Starting the bot..."
  python src/bot.py
else
  echo "Error: src/bot.py not found. Aborting."
  exit 1
fi

# Deactivate the virtual environment
echo "Deactivating virtual environment..."
deactivate