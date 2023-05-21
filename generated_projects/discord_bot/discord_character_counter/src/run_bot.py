import discord
from discord_bot import DiscordCharacterCounterBot
from pathlib import Path
import os


def main():
    # Load the bot token from the environment variable
    bot_token = os.environ.get("DISCORD_BOT_TOKEN")
    if not bot_token:
        raise ValueError("The DISCORD_BOT_TOKEN environment variable is not set.")

    # Initialize and run the DiscordCharacterCounterBot
    bot = DiscordCharacterCounterBot()
    bot.run(bot_token)


if __name__ == "__main__":
    main()
