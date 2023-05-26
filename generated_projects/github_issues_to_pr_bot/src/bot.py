import logging
import time
from pathlib import Path
from typing import Dict, Any

from src.github_api import GitHubAPI


class GitHubIssuesToPRBot:

    def __init__(self, github_api: GitHubAPI, repo: str, polling_interval: int = 10) -> None:
        self.github_api = github_api
        self.repo = repo
        self.polling_interval = polling_interval

    def run(self) -> None:
        while True:
            open_issues = self.github_api.get_open_issues(self.repo)
            for issue in open_issues:
                pr = self.github_api.create_pull_request(self.repo, issue)
                logging.info(f"Created PR for issue #{issue['number']}: {pr['html_url']}")
                self.github_api.add_issue_comment(self.repo, issue['number'], f"Resolved by PR #{pr['number']}: {pr['html_url']}")
                self.github_api.close_issue(self.repo, issue['number'])
                logging.info(f"Closed issue #{issue['number']}")

            time.sleep(self.polling_interval)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    token = Path("TOKEN_FOR_GITHUB").read_text().strip()
    github_api = GitHubAPI(token)
    repo = "Josh-Joseph/github-actions-bot-test"

    bot = GitHubIssuesToPRBot(github_api, repo)
    bot.run()


if __name__ == "__main__":
    main()

