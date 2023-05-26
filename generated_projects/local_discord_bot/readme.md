# Discord Bot Deployed Run Locally

This project contains a Discord bot that allows users to subscribe and receive character count statistics for their messages. The bot listens for messages from its subscribers and responds with a dictionary containing a mapping of each character in the message to a count of the number of times that character appeared in the message.

## Setup and Usage Instructions

1. Ensure you have Python 3.8 or higher installed on your system.
2. Clone the repository to your local machine.
3. Navigate to the `generated_projects/local_discord_bot` directory.
4. Set the `DISCORD_TOKEN` environment variable with your Discord bot token.
   - For example, on Linux or macOS: `export DISCORD_TOKEN=your_token_here`
   - On Windows: `set DISCORD_TOKEN=your_token_here`
5. Go to the Discord Developer Portal and ensure that `intents.message_content` is set to `True` for your bot.
6. Run the bash script `set_up_and_run.sh` to create a Python virtual environment, install the necessary requirements, and start the bot.
7. Invite the bot to your Discord server by following the instructions provided by Discord's developer portal.
8. The bot should be run using the provided bash script and will run indefinitely until it is stopped manually.

## Features

- Users can subscribe to the bot by sending the message "bot I want to subscribe!".
- The bot will confirm subscription by sending the message "You have been subscribed {user}!".
- The bot listens for messages from its subscribers and responds with a dictionary containing a mapping of each character in the message to a count of the number of times that character appeared in the message.
- Users can unsubscribe from the bot by sending the message "bot unsubscribe me!".
- The bot will confirm unsubscription by sending the message "You have been unsubscribed {user}!".

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
