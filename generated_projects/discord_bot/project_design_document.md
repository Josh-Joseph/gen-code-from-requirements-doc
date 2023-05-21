# Discord Bot Design Document

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
The bot will be automatically deployed to Google Compute Engine using GitHub Actions when a commit is merged into the repository.

## Dependency Diagram
```
digraph G {
    run_bot -> discord_bot;
    discord_bot -> discord;
}
```

## File Structure
```
discord_character_counter/
├── .github/
│   └── workflows/
│       └── deploy.yaml
├── src/
│   ├── discord_bot.py
│   └── run_bot.py
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── project_design_document.md
```

## File Descriptions

### src/discord_bot.py
The main discord bot module that handles user subscriptions, message processing, and character counting.
- Third-party packages: discord.py
- `class DiscordCharacterCounterBot(discord.Client)`
  - `async def on_ready(self)`
    - Logs when the bot is ready and connected to Discord.
  - `async def on_message(self, message)`
    - Processes user messages, handles subscriptions, unsubscriptions, and character counting.
- `def count_characters(text: str) -> Dict[str, int]`
  - Counts the characters in the given text and returns a dictionary mapping characters to their counts.

### src/run_bot.py
The entry point for running the discord bot.
- Third-party packages: discord.py
- `def main()`
  - Initializes and runs the DiscordCharacterCounterBot.

### .github/workflows/deploy.yaml
GitHub Actions workflow file for deploying the bot to Google Compute Engine.

### .gitignore
Specifies files and directories to be ignored by git.

### LICENSE
Contains the license for the project.

### README.md
Provides an overview of the project, usage instructions, and other relevant information.

### requirements.txt
Lists the required Python packages for the project.