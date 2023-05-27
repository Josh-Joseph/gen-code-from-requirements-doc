import logging
import requests
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

REPOSITORY = "Josh-Joseph/github-actions-bot-test"


class GitHubAPI:
    def __init__(self, token: str) -> None:
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }

    def branch_exists(self, branch_name: str) -> bool:
        url = f"https://api.github.com/repos/{REPOSITORY}/git/ref/heads/{branch_name}"
        response = requests.get(url, headers=self.headers)
        return response.status_code == 200

    def create_branch(self, issue_number: int) -> None:
        branch_name = f"issue_{issue_number}"
        if self.branch_exists(branch_name):
            logger.info(f"Branch {branch_name} already exists")
            return

        logger.info(f"Creating branch {branch_name}")

        commit_sha = self.get_latest_commit_sha()

        # Create the new branch
        url = f"https://api.github.com/repos/{REPOSITORY}/git/refs"
        data = {
            "ref": f"refs/heads/{branch_name}",
            "sha": commit_sha,
        }
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()

    def pull_request_exists(self, issue_number: int) -> bool:
        pull_requests = self.get_pull_requests()

        for pr in pull_requests:
            if f"Closes #{issue_number}" in pr["body"]:
                return True

        return False

    def create_pull_request(self, issue_number: int, issue_title: str, issue_body: str) -> None:
        if self.pull_request_exists(issue_number):
            logger.info(f"Pull request for issue #{issue_number} already exists")
            return

        branch_name = f"issue_{issue_number}"
        logger.info(f"Creating pull request for branch {branch_name}")

        url = f"https://api.github.com/repos/{REPOSITORY}/pulls"
        data = {
            "title": issue_title,
            "body": f"{issue_body}\n\nCloses #{issue_number}",
            "head": branch_name,
            "base": "main",
        }
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()

    def close_issue(self, issue_number: int) -> None:
        logger.info(f"Closing issue #{issue_number}")

        url = f"https://api.github.com/repos/{REPOSITORY}/issues/{issue_number}"
        data = {
            "state": "closed",
        }
        response = requests.patch(url, json=data, headers=self.headers)
        response.raise_for_status()

    def get_new_issues(self) -> List[Dict[str, Any]]:
        logger.info("Fetching new issues")

        url = f"https://api.github.com/repos/{REPOSITORY}/issues"
        params = {
            "state": "open",
        }
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def is_pull_request_merged(self, pull_request_number: int) -> bool:
        url = f"https://api.github.com/repos/{REPOSITORY}/pulls/{pull_request_number}/merge"
        response = requests.get(url, headers=self.headers)
        return response.status_code == 204

    def merge_pull_request(self, pull_request_number: int) -> None:
        if self.is_pull_request_merged(pull_request_number):
            logger.info(f"Pull request #{pull_request_number} is already merged")
            return

        logger.info(f"Merging pull request #{pull_request_number}")

        url = f"https://api.github.com/repos/{REPOSITORY}/pulls/{pull_request_number}/merge"
        response = requests.put(url, headers=self.headers)
        response.raise_for_status()

    def get_latest_commit_sha(self) -> str:
        url = f"https://api.github.com/repos/{REPOSITORY}/git/ref/heads/main"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()["object"]["sha"]

    def get_pull_requests(self) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{REPOSITORY}/pulls"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
