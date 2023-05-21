from pathlib import Path
import sys

from discord_bot import DiscordBot

def main():
    token_path = Path("token.txt")
    if not token_path.exists():
        print("Error: token.txt not found. Please create a token.txt file with your Discord bot token.")
        sys.exit(1)

    with token_path.open("r") as token_file:
        token = token_file.read().strip()

    bot = DiscordBot()
    bot.run(token)

if __name__ == "__main__":
    main()