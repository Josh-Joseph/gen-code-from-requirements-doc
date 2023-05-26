# GitHub Issues to PR Bot

This bot monitors a GitHub repository for new issues, automatically creates a pull request for each issue, and closes the issue when the pull request is merged. The bot runs indefinitely and checks for changes every 10 seconds.

## Repository

The bot is currently monitoring the following GitHub repository: `Josh-Joseph/github-actions-bot-test`.

## Setup and Usage Instructions

All commands should be run from the root folder of the codebase: `generated_projects/github_issues_to_pr_bot`.

1. Ensure you have Python 3.8 or higher installed on your system.
2. Set the `TOKEN_FOR_GITHUB` environment variable to your GitHub personal access token. See [Obtaining a GitHub Personal Access Token](#obtaining-a-github-personal-access-token) for instructions.
3. Run the bash script `set_up_and_run.sh` to create a Python virtual environment, install necessary requirements, run tests, and start the bot.

## Obtaining a GitHub Personal Access Token

To obtain a GitHub personal access token, follow these steps:

1. Go to your GitHub [settings page](https://github.com/settings/profile).
2. Click on "Developer settings" in the left sidebar.
3. Click on "Personal access tokens" in the left sidebar.
4. Click on the "Generate new token" button.
5. Give your token a descriptive name, and select the "repo" scope.
6. Click on the "Generate token" button at the bottom of the page.
7. Copy the generated token and store it securely, as you won't be able to see it again.

## Features

- Monitors the specified GitHub repository for new issues.
- Creates a new branch and pull request for each new issue.
- Closes the issue and adds a comment with a link to the pull request when the pull request is merged.
- Handles existing open issues when the bot starts.
- Runs indefinitely and checks for changes every 10 seconds.

## Environment Variables

- `TOKEN_FOR_GITHUB`: Your GitHub personal access token. This is required for the bot to interact with the GitHub API.

## Project Structure

```
generated_projects/github_issues_to_pr_bot
├── src
│   ├── __init__.py
│   ├── bot.py
│   └── github_api.py
├── tests
│   ├── __init__.py
│   ├── test_bot.py
│   └── test_github_api.py
├── set_up_and_run.sh
├── requirements.txt
├── LICENSE
├── readme.md
└── project_tech_spec.md
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
