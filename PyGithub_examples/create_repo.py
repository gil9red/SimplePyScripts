#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install pygithub
from github import Github

from config import LOGIN, PASSWORD


# NOTE: delete repo: Settings -> <Danger Zone> -> <Delete this repository>
#       or repo.delete()
NEW_REPO = "Test-Repo"


gh = Github(LOGIN, PASSWORD)
user = gh.get_user()

try:
    repo = user.get_repo(NEW_REPO)

except:
    repo = user.create_repo(NEW_REPO)

print(repo)
