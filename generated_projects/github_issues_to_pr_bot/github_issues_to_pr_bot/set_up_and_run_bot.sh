#!/bin/bash

# Change to the project root directory
cd "$(dirname "$0")"

# Check if the TOKEN_FOR_GITHUB environment variable is set
if [ -z "$TOKEN_FOR_GITHUB" ]; then
  echo "Error: TOKEN_FOR_GITHUB environment variable is not set."
  exit 1
fi

# Install the required packages
pip install -r requirements.txt

# Run the bot
python src/main.py