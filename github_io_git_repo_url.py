#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


# Convertor github pages url to github repo url
# http://nemilya.github.io/coffeescript-game-life/html/game.html
# https://github.com/nemilya/coffeescript-game-life


def github_io_git_repo_url(github_io_url: str) -> str | None:
    match = re.search(r"https?://(.+)\.github\.io/(.+)", github_io_url)
    if match:
        user = match.group(1)
        repo = match.group(2).split("/")[0]

        return f"https://github.com/{user}/{repo}"


if __name__ == "__main__":
    url = "http://nemilya.github.io/coffeescript-game-life/html/game.html"
    print(github_io_git_repo_url(url))
