import threading

import pytest

from src.bot import GitHubIssuesToPRBot
from src.github_api import GitHubAPI


@pytest.fixture
def github_api():
    return GitHubAPI("fake_token")


@pytest.fixture
def bot(github_api):
    return GitHubIssuesToPRBot(github_api, "Josh-Joseph/github-actions-bot-test")


def test_github_issues_to_pr_bot_initialization(github_api, bot):
    assert bot.github_api == github_api
    assert bot.repo == "Josh-Joseph/github-actions-bot-test"
    assert bot.polling_interval == 10


def test_github_issues_to_pr_bot_run_no_issues(github_api, bot, mocker):
    mocker.patch.object(github_api, "get_open_issues", return_value=[])
    mocker.patch.object(bot, "run_once")

    def stop_bot():
        bot.stop()

    timer = threading.Timer(1, stop_bot)
    timer.start()

    bot.run()

    github_api.get_open_issues.assert_called_with("Josh-Joseph/github-actions-bot-test")
    bot.run_once.assert_called_with([])


def test_github_issues_to_pr_bot_run_with_issues(github_api, bot, mocker):
    open_issues = [{"number": 1, "title": "Issue 1", "body": "Issue 1 description"}]
    mocker.patch.object(github_api, "get_open_issues", return_value=open_issues)
    mocker.patch.object(bot, "run_once")

    def stop_bot():
        bot.stop()

    timer = threading.Timer(1, stop_bot)
    timer.start()

    bot.run()

    github_api.get_open_issues.assert_called_with("Josh-Joseph/github-actions-bot-test")
    bot.run_once.assert_called_with(open_issues)


def test_github_issues_to_pr_bot_run_once(github_api, bot, mocker):
    open_issues = [{"number": 1, "title": "Issue 1", "body": "Issue 1 description"}]
    mocker.patch.object(github_api, "create_pull_request")
    mocker.patch.object(github_api, "add_issue_comment")
    mocker.patch.object(github_api, "close_issue")

    bot.run_once(open_issues)

    github_api.create_pull_request.assert_called_with("Josh-Joseph/github-actions-bot-test", open_issues[0])
    github_api.add_issue_comment.assert_called_with("Josh-Joseph/github-actions-bot-test", 1, "This issue has been resolved by PR #2.")
    github_api.close_issue.assert_called_with("Josh-Joseph/github-actions-bot-test", 1)

