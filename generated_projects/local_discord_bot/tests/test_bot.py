import unittest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from src import bot
from src.character_counter import count_characters
from discord import Message


class TestDiscordBot(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        self.discord_bot = bot.DiscordBot()

    @patch("src.bot.DiscordBot.subscribe_user")
    @patch("src.bot.DiscordBot.unsubscribe_user")
    @patch("src.bot.DiscordBot.send_character_count")
    async def test_on_message(self, send_character_count_mock, unsubscribe_user_mock, subscribe_user_mock) -> None:
        message = MagicMock(spec=Message)
        message.content = "bot I want to subscribe!"
        message.author = "TestUser#1234"
        message.reply = AsyncMock()

        await self.discord_bot.on_message(message)
        subscribe_user_mock.assert_called_once_with("TestUser#1234")
        message.reply.assert_called_once_with("You have been subscribed TestUser#1234!")

        message.content = "bot unsubscribe me!"
        await self.discord_bot.on_message(message)
        unsubscribe_user_mock.assert_called_once_with("TestUser#1234")
        message.reply.assert_called_with("You have been unsubscribed TestUser#1234!")

        message.content = "Hello, bot!"
        self.discord_bot.subscribers.add("TestUser#1234")
        await self.discord_bot.on_message(message)
        send_character_count_mock.assert_called_once_with(message)

    def test_subscribe_user(self) -> None:
        self.discord_bot.subscribe_user("TestUser#1234")
        self.assertIn("TestUser#1234", self.discord_bot.subscribers)

    def test_unsubscribe_user(self) -> None:
        self.discord_bot.subscribers.add("TestUser#1234")
        self.discord_bot.unsubscribe_user("TestUser#1234")
        self.assertNotIn("TestUser#1234", self.discord_bot.subscribers)

    async def test_send_character_count(self) -> None:
        message = MagicMock(spec=Message)
        message.content = "Hello, bot!"
        message.author = "TestUser#1234"
        message.reply = AsyncMock()

        with patch("src.character_counter.count_characters", new_callable=AsyncMock) as count_characters_mock:
            count_characters_mock.return_value = {"H": 1, "e": 1, "l": 2, "o": 1, ",": 1, " ": 1, "b": 1, "t": 1, "!": 1}
            await self.discord_bot.send_character_count(message)

        message.reply.assert_called_once_with("{'H': 1, 'e': 1, 'l': 2, 'o': 1, ',': 1, ' ': 1, 'b': 1, 't': 1, '!': 1}")


if __name__ == "__main__":
    unittest.main()
