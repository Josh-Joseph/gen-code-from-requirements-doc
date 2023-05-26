import logging
import os
from typing import Set
import discord
from discord import Intents, Message
from pathlib import Path

from .character_counter import count_characters

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class DiscordBot(discord.Client):
    def __init__(self) -> None:
        intents = Intents.default()
        intents.messages = True
        super().__init__(intents=intents)
        self.subscribers: Set[str] = set()

    async def on_ready(self) -> None:
        logger.info(f"Bot connected as {self.user}")

    async def on_message(self, message: Message) -> None:
        if message.author == self.user:
            return

        content = message.content
        user = str(message.author)

        logger.debug(f"Received message from {user}: {content}")

        if content.lower() == "bot i want to subscribe!":
            self.subscribe_user(user)
            await message.reply(f"You have been subscribed {user}!")
            logger.info(f"Subscribed user {user}")
        elif content.lower() == "bot unsubscribe me!":
            self.unsubscribe_user(user)
            await message.reply(f"You have been unsubscribed {user}!")
            logger.info(f"Unsubscribed user {user}")
        elif user in self.subscribers:
            character_count = count_characters(content)
            await message.reply(str(character_count))
            logger.debug(f"Sent character count to {user}: {character_count}")

    def subscribe_user(self, user: str) -> None:
        self.subscribers.add(user)

    def unsubscribe_user(self, user: str) -> None:
        self.subscribers.discard(user)


def run_bot(token: str) -> None:
    bot = DiscordBot()
    bot.run(token)


if __name__ == "__main__":
    try:
        DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
        run_bot(DISCORD_TOKEN)
    except KeyError:
        logger.error("DISCORD_TOKEN environment variable not set.")
