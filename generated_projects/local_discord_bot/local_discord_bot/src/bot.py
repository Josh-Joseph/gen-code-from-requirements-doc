import os
import logging
import discord
from utils import count_characters

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

class CharacterCountBot(discord.Client):
    """A Discord bot that counts characters in messages from subscribed users."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscribers = set()

    async def on_ready(self):
        """Logs the bot's username and ID when it is ready."""
        logging.info(f"Bot is ready. Username: {self.user.name}, ID: {self.user.id}")

    async def on_message(self, message):
        """
        Processes messages from users, subscribing or unsubscribing them, and
        counting characters in messages from subscribed users.

        Example input-output pair:
        "bot I want to subscribe!" -> "You have been subscribed {user}!"
        """
        if message.author == self.user:
            return

        content = message.content.lower()
        full_username = f"{message.author.name}#{message.author.discriminator}"

        if "bot i want to subscribe!" in content:
            self.subscribers.add(full_username)
            logging.info(f"Subscribed user: {full_username}")
            await message.reply(f"You have been subscribed {full_username}!")
        elif "bot unsubscribe me!" in content:
            if full_username in self.subscribers:
                self.subscribers.remove(full_username)
                logging.info(f"Unsubscribed user: {full_username}")
                await message.reply(f"You have been unsubscribed {full_username}!")
            else:
                await message.reply(f"You are not subscribed {full_username}!")

        if full_username in self.subscribers:
            logging.debug(f"Message received from {full_username}: {message.content}")
            character_count = count_characters(message.content)
            await message.reply(f"Character count: {character_count}")

if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True
    bot = CharacterCountBot(intents=intents)
    bot.run(os.environ["DISCORD_TOKEN"])