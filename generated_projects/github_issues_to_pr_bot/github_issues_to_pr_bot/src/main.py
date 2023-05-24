import logging
import os
import sys
import time
from typing import Dict, List

import requests

from github_api import add_comment_to_issue, close_issue, create_pull_request, get_open_issues

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

POLL_INTERVAL = 10

def main(repo: str) -> None:
    """
    The main function that runs the bot. It monitors the specified GitHub repository for new issues,
    creates a pull request for each issue, and closes the issue when the pull request is merged.

    :param repo: The GitHub repository to monitor, in the format "owner/repo".
    """
    token = os.environ.get("TOKEN_FOR_GITHUB")
    if not token:
        logging.error("Environment variable TOKEN_FOR_GITHUB is not set.")
        sys.exit(1)

    headers = {"Authorization": f"token {token}"}

    while True:
        open_issues = get_open_issues(repo, headers)

        for issue in open_issues:
            if "pull_request" in issue:
                continue

            logging.info(f"Processing issue: {issue['title']}")

            pr = create_pull_request(repo, issue, headers)
            logging.info(f"Created PR: {pr['title']}")

            add_comment_to_issue(
                repo,
                issue["number"],
                f"PR created: {pr['html_url']}",
                headers,
            )

            close_issue(repo, issue["number"], headers)
            logging.info(f"Closed issue: {issue['title']}")

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <repository>")
        sys.exit(1)

    repo = sys.argv[1]
    main(repo)