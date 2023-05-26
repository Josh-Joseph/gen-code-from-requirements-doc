import logging
from typing import Any, Dict, List

import requests


class GitHubAPI:
    def __init__(self, token: str) -> None:
        self.token = token
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def get_open_issues(self, repo: str) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{repo}/issues?state=open"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        issues = response.json()
        return [{"number": issue["number"], "title": issue["title"], "body": issue["body"]} for issue in issues]

    def create_pull_request(self, repo: str, issue: Dict[str, Any]) -> Dict[str, Any]:
        url = f"https://api.github.com/repos/{repo}/pulls"
        branch_name = f"issue-{issue['number']}"
        data = {
            "title": issue["title"],
            "body": f"{issue['body']}\n\nCloses #{issue['number']}",
            "head": branch_name,
            "base": "main",
        }
        response = requests.post(url, json=data, headers=self.headers)
        if response.status_code == 422:
            logging.warning(f"Failed to create pull request for issue {issue['number']}: {response.json()['message']}")
            return None
        response.raise_for_status()
        pr = response.json()
        return {"number": pr["number"], "title": pr["title"], "body": pr["body"]}

    def close_issue(self, repo: str, issue_number: int) -> None:
        url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
        data = {"state": "closed"}
        response = requests.patch(url, json=data, headers=self.headers)
        response.raise_for_status()

    def add_issue_comment(self, repo: str, issue_number: int, comment: str) -> None:
        url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
        data = {"body": comment}
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()

