# Discord Bot Deployed Run Locally

## Overview

The purpose of this discord bot is to allow users to send messages and have those messages characters counted by the bot and sent back to the user as a reply to their message.

## Functional Requirements

- If a user sends a message "bot I want to subscribe!" then the bot will add the user to its subscribers. the bot will confirm subscription by sending the message "You have been subscribed {user}!"
- The user names the bot stores should be their full discord user names
- The bot listens for messages from its subscribers and responds with dictionary containing a mapping of each character in the message to a count of the number of times that character appeared in the message
- A subscriber can be removed from the subscriber list with the message "bot unsubscribe me!". the bot will confirm subscription by sending the message "You have been unsubscribed {user}!"
- All messages sent should be sent as replies to the user's original message.
- The bot will be run locally from a bash script called `set_up_and_run_bot.sh` that will do the following:
  - Create a python virtual environment at `<project_root>/.venv`
  - Install all of the necessary requirements into the virtual environment
  - Start the bot from inside of the virtual environment
- The bot should run indefinitely until it is stopped manually

## Non-functional Requirements

- Use the built-in `logging` module with module-level loggers formatted as `YYYY-MM-DD HH:MM:SS | LEVEL | MESSAGE` where the datetime is in UTC
  - Log all messages received and sent by the bot at the `DEBUG` level
  - Log all actions taken by the bot at the `INFO` level (such as subscribing users or unsubscribing users)
- The discord token is stored in the environment variable named `DISCORD_TOKEN`