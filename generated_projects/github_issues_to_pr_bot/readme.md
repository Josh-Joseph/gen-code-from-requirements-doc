# GitHub Issues to PR Bot

This bot monitors a GitHub repository for new issues and automatically creates a pull request for each issue. It also closes the issue when the pull request is merged. The bot runs indefinitely and checks for changes every 10 seconds.

## Prerequisites

Before running the bot, make sure you have the following environment variable set:

- `TOKEN_FOR_GITHUB`: Your GitHub personal access token with the necessary permissions to create branches, pull requests, and close issues.

## Setup and Usage Instructions

1. Clone the repository to your local machine.
2. Navigate to the root folder of the codebase (`generated_projects/github_issues_to_pr_bot`).
3. Run the bash script `set_up_and_run.sh` to set up the virtual environment, install the required packages, run the tests, and start the bot.

## Code Organization

```
generated_projects/github_issues_to_pr_bot
├── src
│   ├── __init__.py
│   ├── bot.py
│   └── github_api.py
├── tests
│   ├── test_bot.py
│   └── test_github_api.py
├── set_up_and_run.sh
├── requirements.txt
├── readme.md
└── LICENSE
```

## Logging

The built-in `logging` module is used with module-level loggers formatted as `YYYY-MM-DD HH:MM:SS | LEVEL | MESSAGE` where the datetime is in UTC. Log all new occurrences of issues and actions taken by the bot at the `INFO` level.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
