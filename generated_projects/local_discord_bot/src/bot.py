import os
import logging
from typing import List
import discord

from character_counter import count_characters

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class DiscordBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscribers: List[str] = []

    async def on_ready(self) -> None:
        logging.info(f"Bot is ready. Logged in as {self.user}")

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user:
            return

        logging.debug(f"Received message: {message.content}")

        if message.content.lower() == "bot i want to subscribe!":
            self.subscribe_user(str(message.author))
            await message.reply(f"You have been subscribed {message.author}!")
            logging.info(f"Subscribed user: {message.author}")
            return

        if message.content.lower() == "bot unsubscribe me!":
            self.unsubscribe_user(str(message.author))
            await message.reply(f"You have been unsubscribed {message.author}!")
            logging.info(f"Unsubscribed user: {message.author}")
            return

        if self.is_subscribed(str(message.author)):
            character_counts = count_characters(message.content)
            await message.reply(f"Character count: {character_counts}")
            logging.debug(f"Sent character count: {character_counts}")

    def subscribe_user(self, user: str) -> None:
        if user not in self.subscribers:
            self.subscribers.append(user)

    def unsubscribe_user(self, user: str) -> None:
        if user in self.subscribers:
            self.subscribers.remove(user)

    def is_subscribed(self, user: str) -> bool:
        return user in self.subscribers

def main() -> None:
    intents = discord.Intents.default()
    intents.message_content = True

    token = os.environ["DISCORD_TOKEN"]
    client = DiscordBot(intents=intents)
    client.run(token)

if __name__ == "__main__":
    main()
    
