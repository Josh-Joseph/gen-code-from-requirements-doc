import logging
import os
import requests
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

GITHUB_API_BASE_URL = "https://api.github.com"
TOKEN_FOR_GITHUB = os.environ["TOKEN_FOR_GITHUB"]

def get_open_issues(repo: str) -> List[Dict[str, Any]]:
    """
    Retrieves a list of open issues for the given repository.

    :param repo: The GitHub repository in the format "owner/repo".
    :return: A list of dictionaries containing issue data.
    """
    headers = {"Authorization": f"token {TOKEN_FOR_GITHUB}"}
    url = f"{GITHUB_API_BASE_URL}/repos/{repo}/issues?state=open"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def create_pull_request(repo: str, issue: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a pull request for the given issue in the specified repository.

    :param repo: The GitHub repository in the format "owner/repo".
    :param issue: A dictionary containing issue data.
    :return: A dictionary containing the created pull request data.
    """
    headers = {"Authorization": f"token {TOKEN_FOR_GITHUB}"}
    url = f"{GITHUB_API_BASE_URL}/repos/{repo}/pulls"
    data = {
        "title": issue["title"],
        "body": f"{issue['body']}\n\nCloses #{issue['number']}",
        "head": "main",
        "base": "main",
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()

def close_issue(repo: str, issue_id: int) -> None:
    """
    Closes the issue with the given ID in the specified repository.

    :param repo: The GitHub repository in the format "owner/repo".
    :param issue_id: The ID of the issue to close.
    """
    headers = {"Authorization": f"token {TOKEN_FOR_GITHUB}"}
    url = f"{GITHUB_API_BASE_URL}/repos/{repo}/issues/{issue_id}"
    data = {"state": "closed"}
    response = requests.patch(url, json=data, headers=headers)
    response.raise_for_status()

def add_comment_to_issue(repo: str, issue_id: int, comment: str) -> None:
    """
    Adds a comment to the issue with the given ID in the specified repository.

    :param repo: The GitHub repository in the format "owner/repo".
    :param issue_id: The ID of the issue to add a comment to.
    :param comment: The text of the comment to add.
    """
    headers = {"Authorization": f"token {TOKEN_FOR_GITHUB}"}
    url = f"{GITHUB_API_BASE_URL}/repos/{repo}/issues/{issue_id}/comments"
    data = {"body": comment}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()