import discord
from discord.ext import commands
from message_handler import count_characters


class DiscordBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'{self.user} is ready.')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('!subscribe'):
            await self.subscribe_user(message.author)
        elif message.content.startswith('!unsubscribe'):
            await self.unsubscribe_user(message.author)
        else:
            character_count = count_characters(message.content)
            await message.channel.send(f'Character count: {character_count}')

    async def subscribe_user(self, user):
        # Add user to subscribers list (not implemented)
        await user.send('You have been subscribed to the character counter bot.')

    async def unsubscribe_user(self, user):
        # Remove user from subscribers list (not implemented)
        await user.send('You have been unsubscribed from the character counter bot.')
