from pathlib import Path
from typing import Dict, Any
import unittest
from unittest import mock

from src.github_api import GitHubAPI


class TestGitHubAPI(unittest.TestCase):

    def test_github_api_initialization(self) -> None:
        token = "test_token"
        github_api = GitHubAPI(token)
        self.assertEqual(github_api.token, token)

    @mock.patch("src.github_api.requests.get")
    def test_get_open_issues(self, mock_get: mock.MagicMock) -> None:
        mock_get.return_value.json.return_value = [
            {"number": 1, "title": "Issue 1", "body": "Issue 1 description"}
        ]
        repo = "Josh-Joseph/github-actions-bot-test"
        github_api = GitHubAPI("test_token")
        issues = github_api.get_open_issues(repo)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["number"], 1)
        self.assertEqual(issues[0]["title"], "Issue 1")
        self.assertEqual(issues[0]["body"], "Issue 1 description")

    @mock.patch("src.github_api.requests.post")
    def test_create_pull_request(self, mock_post: mock.MagicMock) -> None:
        mock_post.return_value.json.return_value = {
            "number": 2,
            "title": "Issue 1",
            "body": "Issue 1 description\n\nCloses #1"
        }
        repo = "Josh-Joseph/github-actions-bot-test"
        issue = {"number": 1, "title": "Issue 1", "body": "Issue 1 description"}
        github_api = GitHubAPI("test_token")
        pr = github_api.create_pull_request(repo, issue)
        self.assertEqual(pr["number"], 2)
        self.assertEqual(pr["title"], "Issue 1")
        self.assertEqual(pr["body"], "Issue 1 description\n\nCloses #1")

    @mock.patch("src.github_api.requests.patch")
    def test_close_issue(self, mock_patch: mock.MagicMock) -> None:
        repo = "Josh-Joseph/github-actions-bot-test"
        issue_number = 1
        github_api = GitHubAPI("test_token")
        github_api.close_issue(repo, issue_number)
        mock_patch.assert_called_once()

    @mock.patch("src.github_api.requests.post")
    def test_add_issue_comment(self, mock_post: mock.MagicMock) -> None:
        repo = "Josh-Joseph/github-actions-bot-test"
        issue_number = 1
        comment = "This issue has been resolved by PR #2."
        github_api = GitHubAPI("test_token")
        github_api.add_issue_comment(repo, issue_number, comment)
        mock_post.assert_called_once()


if __name__ == "__main__":
    unittest.main()
