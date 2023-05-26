import logging
import os
import time
from pathlib import Path
from typing import Dict

from .github_api import create_branch, create_pull_request, close_issue, get_open_issues, is_pull_request_created, is_pull_request_merged, get_pull_request_url

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

CHECK_INTERVAL = 10
TOKEN = os.environ["TOKEN_FOR_GITHUB"]


def get_repo_name() -> str:
    return os.environ.get("REPO_NAME", "Josh-Joseph/github-actions-bot-test")


def main() -> None:
    repo_name = get_repo_name()
    logging.info(f"Bot started for repository: {repo_name}")
    handle_existing_issues(repo_name)

    while True:
        issues = get_open_issues(repo_name)
        for issue in issues:
            issue_number = issue["number"]
            issue_title = issue["title"]
            issue_body = issue["body"]

            if not is_pull_request_created(repo_name, issue_number):
                logging.info(f"Creating PR for issue #{issue_number}")
                create_branch(repo_name, issue_number)
                create_pull_request(repo_name, issue_number, issue_title, issue_body)

            if is_pull_request_merged(repo_name, issue_number):
                logging.info(f"Closing issue #{issue_number}")
                pull_request_url = get_pull_request_url(repo_name, issue_number)
                close_issue(repo_name, issue_number, pull_request_url)

        time.sleep(CHECK_INTERVAL)


def handle_existing_issues(repo_name: str) -> None:
    issues = get_open_issues(repo_name)
    for issue in issues:
        issue_number = issue["number"]
        issue_title = issue["title"]
        issue_body = issue["body"]

        if not is_pull_request_created(repo_name, issue_number):
            logging.info(f"Creating PR for existing issue #{issue_number}")
            create_branch(repo_name, issue_number)
            create_pull_request(repo_name, issue_number, issue_title, issue_body)


if __name__ == "__main__":
    main()
