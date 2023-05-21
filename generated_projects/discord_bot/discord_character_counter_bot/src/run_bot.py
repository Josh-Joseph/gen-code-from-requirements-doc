import os
from pathlib import Path
from dotenv import load_dotenv
from src.bot import CharacterCounterBot


def main():
    # Load environment variables from .env file
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    # Get the Discord bot token
    token = os.getenv('DISCORD_TOKEN')

    # Initialize and run the bot
    bot = CharacterCounterBot()
    bot.run(token)


if __name__ == '__main__':
    main()
