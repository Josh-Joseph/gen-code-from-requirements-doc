# Local Discord Bot

This Discord bot allows users to subscribe and have their messages' characters counted by the bot. The bot will reply with a dictionary containing a mapping of each character in the message to a count of the number of times that character appeared in the message.

## Setup and Usage Instructions

1. Clone the repository.
2. Set the `DISCORD_TOKEN` environment variable with your Discord bot token.
3. Run the `set_up_and_run_bot.sh` script to create a virtual environment, install the necessary requirements, and start the bot.

## Features

- Users can subscribe and unsubscribe to the bot by sending messages.
- The bot listens for messages from its subscribers and responds with a dictionary containing a mapping of each character in the message to a count of the number of times that character appeared in the message.
- The bot runs indefinitely until it is stopped manually.

For more information, please refer to the [Project Design Document](project_design_document.md).