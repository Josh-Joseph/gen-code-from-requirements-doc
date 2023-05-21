import discord
from typing import Dict


class CharacterCounterBot(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        character_count = count_characters(message.content)
        response = f'Character count: {character_count}'
        await message.channel.send(response)

        
def count_characters(text: str) -> Dict[str, int]:
    character_count = {}
    for char in text:
        if char in character_count:
            character_count[char] += 1
        else:
            character_count[char] = 1
    return character_count