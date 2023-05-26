import unittest
from unittest.mock import patch
import logging

from src import bot


class TestBot(unittest.TestCase):

    @patch("src.bot.handle_existing_issues")
    @patch("src.bot.time.sleep")
    def test_main(self, mock_sleep, mock_handle_existing_issues):
        with patch("src.bot.logging") as mock_logging:
            with self.assertRaises(SystemExit):
                bot.main()
                mock_handle_existing_issues.assert_called_once()
                mock_sleep.assert_called_with(10)
                mock_logging.basicConfig.assert_called_once_with(
                    level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )

    @patch("src.bot.github_api.get_open_issues")
    @patch("src.bot.github_api.create_branch")
    @patch("src.bot.github_api.create_pull_request")
    def test_handle_existing_issues(self, mock_create_pull_request, mock_create_branch, mock_get_open_issues):
        mock_get_open_issues.return_value = [
            {"number": 1, "title": "Issue 1", "body": "Issue 1 body"},
            {"number": 2, "title": "Issue 2", "body": "Issue 2 body"},
        ]

        bot.handle_existing_issues()

        mock_create_branch.assert_any_call(1)
        mock_create_branch.assert_any_call(2)
        mock_create_pull_request.assert_any_call(1, "Issue 1", "Issue 1 body")
        mock_create_pull_request.assert_any_call(2, "Issue 2", "Issue 2 body")

    @patch("src.bot.github_api.get_open_issues")
    @patch("src.bot.github_api.create_branch")
    @patch("src.bot.github_api.create_pull_request")
    def test_handle_existing_issues_no_open_issues(self, mock_create_pull_request, mock_create_branch, mock_get_open_issues):
        mock_get_open_issues.return_value = []

        bot.handle_existing_issues()

        mock_create_branch.assert_not_called()
        mock_create_pull_request.assert_not_called()

    @patch("src.bot.github_api.get_open_issues")
    @patch("src.bot.github_api.create_branch")
    @patch("src.bot.github_api.create_pull_request")
    def test_handle_existing_issues_exception(self, mock_create_pull_request, mock_create_branch, mock_get_open_issues):
        mock_get_open_issues.side_effect = Exception("Error occurred")

        with self.assertRaises(Exception):
            bot.handle_existing_issues()

        mock_create_branch.assert_not_called()
        mock_create_pull_request.assert_not_called()


if __name__ == "__main__":
    unittest.main()
