# GitHub Issues to PR Bot

## Overview

The purpose of this bot is to monitor for issues that are created in a GitHub repository and automatically create a pull request for each issue. It will also automatically close the issue when the pull request is merged.

## Functional Requirements

- The bot must be run by a bash script `<project_root>/set_up_and_run.sh` that will do the following:
  - Creates a python virtual environment at `<project_root>/.venv`
  - Installs all of the necessary requirements into the virtual environment
  - Starts the bot from inside of the virtual environment
- The bot must monitor the GitHub repository `Josh-Joseph/github-actions-bot-test` for new issues
- When a new issue is created, the bot must:
  - Create a new branch with the issue number as the branch name.
  - Create a pull request from the new branch to main with:
    - The issue's title as the pull request's title
    - The issue's body as the pull request's body
    - A link to the issue
- When the pull request is merged, the bot must add a comment to the issue with a link to the pull request and close the issue.
- If there are issues open when the bot is started, the bot must create pull requests for those issues.
- The bot should check for changes every 10 seconds and log at the `INFO` level when it checks.
- The bot should run indefinitely.

## Non-functional Requirements

- Use the built-in `logging` module with module-level loggers formatted as `YYYY-MM-DD HH:MM:SS | LEVEL | MESSAGE` where the datetime is in UTC.
  - Log all new occurrences of issues and actions taken by the bot at the `INFO` level.
- The GitHub token is stored in the environment variable named `TOKEN_FOR_GITHUB`.
- Inside the bash script that runs the bot, make sure to:
    - Create the virtual environment, activate it, install the required packages
    - Run the tests
    - Start the bot
- Use the MIT license for the project