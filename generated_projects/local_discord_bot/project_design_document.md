# Project Design Document

## Table of Contents

- [Last Updated](#last-updated)
- [Overview](#overview)
- [Setup and Usage Instructions](#setup-and-usage-instructions)
- [Dependency Diagram](#dependency-diagram)
- [File Structure](#file-structure)
- [Logging](#logging)
- [set_up_and_run_bot.sh](#set_up_and_run_botsh)
- [src/bot.py](#srcbotpy)
- [src/utils.py](#srcutilspy)
- [requirements.txt](#requirementstxt)
- [readme.md](#readmemd)
- [LICENSE](#license)

## Last Updated

2023-05-22

## Overview

The purpose of this project is to create a Discord bot that allows users to subscribe and have their messages' characters counted by the bot. The bot will then send a reply to the user with a dictionary containing a mapping of each character in the message to the number of times that character appeared in the message.

## Setup and Usage Instructions

1. Clone the repository.
2. Set the `DISCORD_TOKEN` environment variable with your Discord bot token.
3. Run the `set_up_and_run_bot.sh` script to set up the virtual environment, install the necessary requirements, and start the bot.

## Dependency Diagram

```graphviz
digraph G {
    "set_up_and_run_bot.sh" -> "requirements.txt";
    "set_up_and_run_bot.sh" -> "src/bot.py";
    "src/bot.py" -> "src/utils.py";
}
```

## File Structure

```
local_discord_bot
├── .venv
├── set_up_and_run_bot.sh
├── src
│   ├── bot.py
│   └── utils.py
├── requirements.txt
├── readme.md
└── LICENSE
```

## Logging

The built-in `logging` module will be used with module-level loggers formatted as `YYYY-MM-DD HH:MM:SS | LEVEL | MESSAGE` where the datetime is in UTC. Log all messages received and sent by the bot at the `DEBUG` level and all actions taken by the bot at the `INFO` level (such as subscribing users or unsubscribing users).

## set_up_and_run_bot.sh

A bash script that sets up the Python virtual environment, installs the necessary requirements, and starts the bot.

## src/bot.py

The main file for the Discord bot that handles subscribing and unsubscribing users, listening for messages, and sending replies with character counts.

- Third-party Python packages: discord.py
- Environment variables: DISCORD_TOKEN

- `class DiscordBotClient(discord.Client)`
  - The main class for the Discord bot that inherits from `discord.Client`.

  - `async def on_ready(self)`
    - Called when the bot is ready and connected to Discord.
    - Logs the bot's username and ID.

  - `async def on_message(self, message)`
    - Called when a message is received.
    - Handles subscribing and unsubscribing users, and sending replies with character counts.

## src/utils.py

Utility functions for the Discord bot.

- `def count_characters(text: str) -> Dict[str, int]`
  - Counts the occurrences of each character in the given text.
  - Example input-output pair: `count_characters("hello") -> {"h": 1, "e": 1, "l": 2, "o": 1}`

## requirements.txt

A list of required Python packages for the project.

## readme.md

A readme file containing an overview of the project, setup and usage instructions, and other relevant information.

## LICENSE

A file containing the license for the project.