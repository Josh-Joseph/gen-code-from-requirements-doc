import discord
from message_handler import MessageHandler


class DiscordBot(discord.Client):
    def __init__(self, message_handler: MessageHandler):
        super().__init__()
        self.message_handler = message_handler

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        character_count = self.message_handler.process_message(message.content)
        reply = f'Your message has {character_count} characters.'
        await message.channel.send(reply)


if __name__ == '__main__':
    message_handler = MessageHandler()
    bot = DiscordBot(message_handler)
    bot.run('your-token-here')