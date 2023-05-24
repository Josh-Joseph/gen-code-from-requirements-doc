import logging
import requests
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

GITHUB_API_BASE_URL = "https://api.github.com"
TOKEN_FOR_GITHUB = "TOKEN_FOR_GITHUB"

def get_open_issues(repo: str) -> List[Dict[str, Any]]:
    headers = {"Authorization": f"token {TOKEN_FOR_GITHUB}"}
    url = f"{GITHUB_API_BASE_URL}/repos/{repo}/issues?state=open"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def create_pull_request(repo: str, issue: Dict[str, Any]) -> Dict[str, Any]:
    headers = {"Authorization": f"token {TOKEN_FOR_GITHUB}"}
    url = f"{GITHUB_API_BASE_URL}/repos/{repo}/pulls"
    data = {
        "title": issue["title"],
        "body": f"{issue['body']}\n\nIssue: #{issue['number']}",
        "head": f"issue-{issue['number']}",
        "base": "main",
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()

def close_issue(repo: str, issue_id: int) -> None:
    headers = {"Authorization": f"token {TOKEN_FOR_GITHUB}"}
    url = f"{GITHUB_API_BASE_URL}/repos/{repo}/issues/{issue_id}"
    data = {"state": "closed"}
    response = requests.patch(url, json=data, headers=headers)
    response.raise_for_status()

def add_comment_to_issue(repo: str, issue_id: int, comment: str) -> None:
    headers = {"Authorization": f"token {TOKEN_FOR_GITHUB}"}
    url = f"{GITHUB_API_BASE_URL}/repos/{repo}/issues/{issue_id}/comments"
    data = {"body": comment}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()