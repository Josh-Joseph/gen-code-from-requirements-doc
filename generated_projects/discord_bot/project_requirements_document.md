# Disocrd Bot

## Overview

The purpose of this discord bot is to allow users to send messages and have those messages characters counted by the bot and sent back to the user as a reply to their message.

## Functional Requirements

- If a user sends a message "bot I want to subscribe!" then the bot will add the user to its subscribers. the bot will confirm subscription by sending the message "You have been subscribed {user}!"
- The user names the bot stores should be their full discord user names
- The bot listens for messages from its subscribers and responds with dictionary containing a mapping of each character in the message to a count of the number of times that character appeared in the message
- A subscriber can be removed from the subscriber list with the message "bot unsubscribe me!". the bot will confirm subscription by sending the message "You have been unsubscribed {user}!"
- All messages sent should be sent as replies to the user's original message.
- The bot must be started with the command `python run_bot.py`
- The command `python run_bot.py` must be run from inside of python virtual environment placed at `<project_root>/.venv` that has all of the necessary requirements installed
- Everytime a commit is merged into the repository, GitHub actions must deploy the bot to Google Compute Engine.

## Non-functional Requirements

- Use the built-in `logging` module to log at key points in the code. Create module-level loggers with `datefmt='%Y-%m-%d %H:%M:%S'`