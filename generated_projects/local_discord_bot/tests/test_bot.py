import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from src import bot


class TestBot(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.discord_bot = bot.DiscordBot()

    @patch.object(bot.DiscordBot, "subscribe_user")
    def test_subscribe_user(self, mock_subscribe_user):
        user = "JohnDoe#1234"
        self.discord_bot.subscribe_user(user)
        mock_subscribe_user.assert_called_once_with(user)

    @patch.object(bot.DiscordBot, "unsubscribe_user")
    def test_unsubscribe_user(self, mock_unsubscribe_user):
        user = "JohnDoe#1234"
        self.discord_bot.unsubscribe_user(user)
        mock_unsubscribe_user.assert_called_once_with(user)

    @patch.object(bot.DiscordBot, "is_subscribed")
    def test_is_subscribed(self, mock_is_subscribed):
        user = "JohnDoe#1234"
        self.discord_bot.is_subscribed(user)
        mock_is_subscribed.assert_called_once_with(user)

    async def test_on_message_subscribe(self):
        message = MagicMock()
        message.content = "bot I want to subscribe!"
        message.author = "JohnDoe#1234"
        message.reply = AsyncMock()

        await self.discord_bot.on_message(message)
        self.discord_bot.subscribe_user.assert_called_once_with(message.author)
        await message.reply.assert_called_once()

    async def test_on_message_unsubscribe(self):
        message = MagicMock()
        message.content = "bot unsubscribe me!"
        message.author = "JohnDoe#1234"
        message.reply = AsyncMock()

        await self.discord_bot.on_message(message)
        self.discord_bot.unsubscribe_user.assert_called_once_with(message.author)
        await message.reply.assert_called_once()

    async def test_on_message_character_count(self):
        message = MagicMock()
        message.content = "test message"
        message.author = "JohnDoe#1234"
        message.reply = AsyncMock()

        with patch.object(bot.DiscordBot, "is_subscribed", return_value=True):
            await self.discord_bot.on_message(message)

        await message.reply.assert_called_once()

    async def test_on_message_ignore_bot(self):
        message = MagicMock()
        message.content = "test message"
        message.author = self.discord_bot.user
        message.reply = AsyncMock()

        await self.discord_bot.on_message(message)
        message.reply.assert_not_called()


if __name__ == "__main__":
    unittest.main()
