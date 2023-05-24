import os
import logging
from typing import Dict
import discord
from discord import Message
from discord import User
from discord import PartialMessage
from src.utils import count_characters

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

class CharacterCountBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscribers: Dict[str, User] = {}

    async def on_ready(self) -> None:
        logging.info(f"Bot is ready. Logged in as {self.user}")

    async def on_message(self, message: Message) -> None:
        if message.author == self.user:
            return

        content = message.content
        logging.debug(f"Received message from {message.author}: {content}")

        if content.lower() == "bot i want to subscribe!":
            self.subscribers[message.author.name] = message.author
            logging.info(f"Subscribed user {message.author}")
            await message.reply(f"You have been subscribed {message.author}!")
        elif content.lower() == "bot unsubscribe me!":
            if message.author.name in self.subscribers:
                del self.subscribers[message.author.name]
                logging.info(f"Unsubscribed user {message.author}")
                await message.reply(f"You have been unsubscribed {message.author}!")
        elif message.author.name in self.subscribers:
            character_counts = count_characters(content)
            logging.debug(f"Sending character count to {message.author}: {character_counts}")
            await message.reply(str(character_counts))

def main() -> None:
    intents = discord.Intents.default()
    intents.message_content = True
    bot = CharacterCountBot(intents=intents)
    bot.run(os.environ["DISCORD_TOKEN"])

if __name__ == "__main__":
    main()