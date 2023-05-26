import os
import unittest
from unittest.mock import patch

from src import github_api


class TestGitHubAPI(unittest.TestCase):

    @patch("src.github_api.requests.post")
    def test_create_branch(self, mock_post):
        github_api.create_branch(1)
        headers = {"Authorization": f"token {os.environ['TOKEN_FOR_GITHUB']}"}
        mock_post.assert_called_once_with(
            "https://api.github.com/repos/Josh-Joseph/github-actions-bot-test/git/refs",
            headers=headers,
            json={"ref": "refs/heads/1", "sha": "main"}
        )

    @patch("src.github_api.requests.post")
    def test_create_pull_request(self, mock_post):
        github_api.create_pull_request(1, "Issue Title", "Issue Body")
        headers = {"Authorization": f"token {os.environ['TOKEN_FOR_GITHUB']}"}
        mock_post.assert_called_once_with(
            "https://api.github.com/repos/Josh-Joseph/github-actions-bot-test/pulls",
            headers=headers,
            json={
                "title": "Issue Title",
                "body": "Issue Body\n\nIssue: https://github.com/Josh-Joseph/github-actions-bot-test/issues/1",
                "head": "1",
                "base": "main"
            }
        )

    @patch("src.github_api.requests.post")
    @patch("src.github_api.requests.patch")
    def test_close_issue(self, mock_patch, mock_post):
        github_api.close_issue(1, "https://github.com/pulls/1")
        headers = {"Authorization": f"token {os.environ['TOKEN_FOR_GITHUB']}"}
        mock_post.assert_called_once_with(
            "https://api.github.com/repos/Josh-Joseph/github-actions-bot-test/issues/1/comments",
            headers=headers,
            json={"body": "This issue has been resolved by PR: https://github.com/pulls/1"}
        )
        mock_patch.assert_called_once_with(
            "https://api.github.com/repos/Josh-Joseph/github-actions-bot-test/issues/1",
            headers=headers,
            json={"state": "closed"}
        )


if __name__ == "__main__":
    unittest.main()
