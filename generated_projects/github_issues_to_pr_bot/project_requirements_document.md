# GitHub Issues to PR Bot

## Overview

The purpose of this bot is to monitor for issues that are created in a GitHub repository and automatically create a pull request for each issue. It will also automatically close the issue when the pull request is merged.

## Functional Requirements

- The bot will be run with `<project_root>/set_up_and_run_bot.sh`
- The bot will monitor the GitHub repository `Josh-Joseph/github-actions-bot-test` for new issues
- When a new issue is created, the bot will create a pull request with the issue's title as the pull request's title, the issue's body as the pull request's body, and a link to the issue.
- When the pull request is merged, the bot will add a comment to the issue with a link to the pull request and close the issue.
- The bot should run indefinitely until it is stopped manually

## Non-functional Requirements

- Use the built-in `logging` module with module-level loggers formatted as `YYYY-MM-DD HH:MM:SS | LEVEL | MESSAGE` where the datetime is in UTC
  - Log all new occurrences of issues and actions taken by the bot at the `INFO` level
- The GitHub token is stored in the environment variable named `TOKEN_FOR_GITHUB`