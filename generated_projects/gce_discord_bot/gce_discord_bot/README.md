# GCE Discord Bot

This is a Discord bot that counts the characters in a user's message and sends the count back as a reply. The bot is deployed to Google Compute Engine using GitHub Actions.

## Table of Contents
- [Setup Instructions](#setup-instructions)
- [Usage Instructions](#usage-instructions)
- [Deployment Instructions](#deployment-instructions)

## Setup Instructions
1. Clone the repository
2. Create a virtual environment in the project root directory with `python -m venv .venv`
3. Activate the virtual environment with `source .venv/bin/activate`
4. Install the required packages with `pip install -r requirements.txt`

## Usage Instructions
1. Run the bot with `python run_bot.py`
2. Send a message in a Discord channel where the bot is present
3. The bot will reply with the character count of your message

## Deployment Instructions
The bot will be deployed to Google Compute Engine using GitHub Actions each time a commit is merged into the repository.