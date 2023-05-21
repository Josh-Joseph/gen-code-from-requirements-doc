import discord
from typing import Dict


class DiscordCharacterCounterBot(discord.Client):
    async def on_ready(self):
        print(f"We have logged in as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith("!count"):
            character_counts = count_characters(message.content[6:])
            response = "Character counts:\n"
            for char, count in character_counts.items():
                response += f"{char}: {count}\n"
            await message.channel.send(response)


def count_characters(text: str) -> Dict[str, int]:
    character_counts = {}
    for char in text:
        if char in character_counts:
            character_counts[char] += 1
        else:
            character_counts[char] = 1
    return character_counts