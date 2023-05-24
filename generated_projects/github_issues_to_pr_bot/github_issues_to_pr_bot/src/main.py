import os
import time
import logging
from typing import Dict, Any
import requests
from src.github_api import get_open_issues, create_pull_request, close_issue, add_comment_to_issue

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

GITHUB_REPO = "Josh-Joseph/github-actions-bot-test"
POLL_INTERVAL = 10

def main() -> None:
    token = os.environ["TOKEN_FOR_GITHUB"]
    headers = {"Authorization": f"token {token}"}

    while True:
        logging.info("Checking for new issues...")
        open_issues = get_open_issues(GITHUB_REPO, headers)

        for issue in open_issues:
            logging.info(f"Creating pull request for issue {issue['number']}...")
            pr = create_pull_request(GITHUB_REPO, issue, headers)
            logging.info(f"Pull request {pr['number']} created for issue {issue['number']}.")

            logging.info(f"Closing issue {issue['number']}...")
            close_issue(GITHUB_REPO, issue["number"], headers)
            logging.info(f"Issue {issue['number']} closed.")

            logging.info(f"Adding comment to issue {issue['number']}...")
            comment = f"Pull request #{pr['number']} has been created and merged. Issue closed."
            add_comment_to_issue(GITHUB_REPO, issue["number"], comment, headers)
            logging.info(f"Comment added to issue {issue['number']}.")

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()