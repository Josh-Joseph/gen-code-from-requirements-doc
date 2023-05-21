import os
from pathlib import Path
from dotenv import load_dotenv
from discord_bot import DiscordBot

def main():
    # Load environment variables
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    # Initialize the Discord bot
    token = os.getenv('DISCORD_TOKEN')
    bot = DiscordBot()

    # Run the bot
    bot.run(token)

if __name__ == '__main__':
    main()