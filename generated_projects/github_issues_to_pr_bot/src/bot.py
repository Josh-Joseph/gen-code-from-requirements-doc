import asyncio
import logging
import os
import time
from pathlib import Path

from github_api import GitHubAPI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

REPOSITORY = "Josh-Joseph/github-actions-bot-test"
TOKEN = os.environ["TOKEN_FOR_GITHUB"]
CHECK_INTERVAL = 10


async def main() -> None:
    github_api = GitHubAPI(token=TOKEN)
    await monitor_repository(github_api=github_api)


async def monitor_repository(github_api: GitHubAPI) -> None:
    while True:
        new_issues = await github_api.get_new_issues(repository=REPOSITORY)

        for issue in new_issues:
            issue_number = issue["number"]
            issue_title = issue["title"]
            issue_body = issue["body"]

            logger.info(f"New issue detected: #{issue_number} - {issue_title}")

            await github_api.create_branch(issue_number=issue_number, repository=REPOSITORY)
            logger.info(f"Created branch for issue #{issue_number}")

            await github_api.create_pull_request(
                issue_number=issue_number,
                issue_title=issue_title,
                issue_body=issue_body,
                repository=REPOSITORY,
            )
            logger.info(f"Created pull request for issue #{issue_number}")

        await asyncio.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())

