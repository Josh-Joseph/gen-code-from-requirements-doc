#!/bin/bash

# Create a python virtual environment at <project_root>/.venv
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install all of the necessary requirements into the virtual environment
pip install -r requirements.txt

# Start the bot from inside of the virtual environment
python src/bot.py