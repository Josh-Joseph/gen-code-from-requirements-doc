import unittest
from unittest.mock import MagicMock, patch
from src.github_api import GitHubAPI


class TestGitHubAPI(unittest.TestCase):
    """Test cases for the GitHubAPI class."""

    def setUp(self):
        self.token = "test_token"
        self.github_api = GitHubAPI(self.token)

    @patch("src.github_api.requests")
    def test_create_branch(self, mock_requests):
        """Test the create_branch method."""
        issue_number = 1
        self.github_api.create_branch(issue_number)
        mock_requests.post.assert_called_once()

    @patch("src.github_api.requests")
    def test_create_pull_request(self, mock_requests):
        """Test the create_pull_request method."""
        issue_number = 1
        issue_title = "Test Issue"
        issue_body = "This is a test issue."
        self.github_api.create_pull_request(issue_number, issue_title, issue_body)
        mock_requests.post.assert_called_once()

    @patch("src.github_api.requests")
    def test_close_issue(self, mock_requests):
        """Test the close_issue method."""
        issue_number = 1
        self.github_api.close_issue(issue_number)
        mock_requests.patch.assert_called_once()

    @patch("src.github_api.requests")
    def test_get_new_issues(self, mock_requests):
        """Test the get_new_issues method."""
        mock_requests.get.return_value.json.return_value = [{"number": 1, "title": "Test Issue", "body": "This is a test issue."}]
        new_issues = self.github_api.get_new_issues()
        self.assertEqual(len(new_issues), 1)
        self.assertEqual(new_issues[0]["number"], 1)
        self.assertEqual(new_issues[0]["title"], "Test Issue")
        self.assertEqual(new_issues[0]["body"], "This is a test issue.")
        mock_requests.get.assert_called_once()

    @patch("src.github_api.requests")
    def test_merge_pull_request(self, mock_requests):
        """Test the merge_pull_request method."""
        pull_request_number = 1
        self.github_api.merge_pull_request(pull_request_number)
        mock_requests.put.assert_called_once()


if __name__ == "__main__":
    unittest.main()
    
