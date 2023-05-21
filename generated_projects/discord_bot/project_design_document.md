# Discord Bot Project Design Document

## Table of Contents
- [Last Updated](#last-updated)
- [Overview](#overview)
- [Usage Instructions](#usage-instructions)
  - [Setup Instructions](#setup-instructions)
- [Deployment Instructions](#deployment-instructions)
- [Dependency Diagram](#dependency-diagram)
- [File Structure](#file-structure)
- [File Descriptions](#file-descriptions)

## Last Updated
2023-05-21

## Overview
The purpose of this discord bot is to allow users to send messages and have those messages characters counted by the bot and sent back to the user as a reply to their message.

## Usage Instructions

### Setup Instructions
1. Clone the repository
2. Create a virtual environment in the project root directory with `python -m venv .venv`
3. Activate the virtual environment with `source .venv/bin/activate`
4. Install the required packages with `pip install -r requirements.txt`
5. Run the bot with `python run_bot.py`

## Deployment Instructions
The bot will be deployed to Google Compute Engine using GitHub Actions. The deployment process will be triggered every time a commit is merged into the repository.

## Dependency Diagram
```graphviz
digraph G {
    run_bot -> bot;
    bot -> discord;
    bot -> logging;
}
```

## File Structure
```
discord_character_counter_bot/
├── .github/
│   └── workflows/
│       └── deploy.yaml
├── .venv/
├── src/
│   ├── bot.py
│   └── run_bot.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## File Descriptions

### src/bot.py
Contains the main bot logic for handling messages and managing subscribers.
- Third-party packages: discord.py
- `class CharacterCounterBot`: The main bot class that extends discord.Client.
  - `async def on_ready(self)`: Logs when the bot is ready and connected to Discord.
  - `async def on_message(self, message)`: Handles incoming messages and processes them based on the content.
- `def count_characters(text: str) -> Dict[str, int]`: Counts the characters in the given text and returns a dictionary with character counts.

### src/run_bot.py
The entry point for running the bot.
- Third-party packages: discord.py
- `def main()`: Initializes and runs the bot.

### .github/workflows/deploy.yaml
GitHub Actions workflow file for deploying the bot to Google Compute Engine.

### .gitignore
Specifies files and directories to be ignored by git.

### LICENSE
Contains the license for the project.

### README.md
Provides an overview of the project and instructions for setup and usage.

### requirements.txt
Lists the required Python packages for the project.