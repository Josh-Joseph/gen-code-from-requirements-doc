import unittest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from src import bot


class TestBotFunctions(unittest.IsolatedAsyncioTestCase):

    @patch("src.bot.monitor_repository")
    async def test_main_calls_monitor_repository(self, mock_monitor_repository):
        with patch("src.bot.GitHubAPI") as mock_github_api_class:
            mock_github_api = AsyncMock()
            mock_github_api_class.return_value = mock_github_api
            await bot.main()
            mock_monitor_repository.assert_called_once()

    @patch("src.bot.GitHubAPI")
    async def test_monitor_repository_creates_branch_and_pull_request(self, mock_github_api_class):
        mock_github_api = AsyncMock()
        mock_github_api_class.return_value = mock_github_api
        mock_github_api.get_new_issues.return_value = [
            {
                "number": 1,
                "title": "Test Issue",
                "body": "This is a test issue."
            }
        ]

        await bot.monitor_repository(mock_github_api)

        mock_github_api.create_branch.assert_called_once_with(1)
        mock_github_api.create_pull_request.assert_called_once_with(1, "Test Issue", "This is a test issue.")
        mock_github_api.close_issue.assert_not_called()

    @patch("src.bot.GitHubAPI")
    async def test_monitor_repository_closes_merged_pull_request(self, mock_github_api_class):
        mock_github_api = AsyncMock()
        mock_github_api_class.return_value = mock_github_api
        mock_github_api.get_new_issues.return_value = [
            {
                "number": 1,
                "title": "Test Issue",
                "body": "This is a test issue.",
                "pull_request": {
                    "merged": True
                }
            }
        ]

        await bot.monitor_repository(mock_github_api)

        mock_github_api.create_branch.assert_not_called()
        mock_github_api.create_pull_request.assert_not_called()
        mock_github_api.close_issue.assert_called_once_with(1)

    @patch("src.bot.GitHubAPI")
    async def test_monitor_repository_no_new_issues(self, mock_github_api_class):
        mock_github_api = AsyncMock()
        mock_github_api_class.return_value = mock_github_api
        mock_github_api.get_new_issues.return_value = []

        await bot.monitor_repository(mock_github_api)

        mock_github_api.create_branch.assert_not_called()
        mock_github_api.create_pull_request.assert_not_called()
        mock_github_api.close_issue.assert_not_called()

    @patch("asyncio.sleep")
    async def test_monitor_repository_sleeps_for_10_seconds(self, mock_sleep):
        with patch("src.bot.GitHubAPI") as mock_github_api_class:
            mock_github_api = AsyncMock()
            mock_github_api_class.return_value = mock_github_api
            mock_github_api.get_new_issues.return_value = []

            await bot.monitor_repository(mock_github_api)

            mock_sleep.assert_called_once_with(10)


if __name__ == "__main__":
    unittest.main()
