#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install pygithub
from github import Github

from config import LOGIN, PASSWORD


gh = Github(LOGIN, PASSWORD)
# #
# # OR:
# # But: "github.GithubException.RateLimitExceededException: 403 {'message': "API rate limit exceeded for \
# # 79.000.10.000. (But here's the good news: Authenticated requests get a higher rate limit. Check out the
# # documentation for more details.)", 'documentation_url': 'https://developer.github.com/v3/#rate-limiting'}"
# gh = Github()

gist = gh.get_gist("2f80a34fb601cd685353")
print(gist)
print(f"created_at: {gist.created_at}, updated_at: {gist.updated_at}")
print()

print(f"files ({len(gist.files)}): {gist.files}")
print()

print(f"history ({len(gist.history)}):")

# From new to old:
# for history in gist.history:
#
# Or:
# for history in reversed(gist.history):
#
# First 10:
for history in list(reversed(gist.history))[:10]:
    print(
        f"  committed_at: {history.committed_at}, version: {history.version}, files: {history.files}"
    )

    file = history.files["gistfile1.txt"]
    print(f"    url: {file.raw_url}")
    print(f"    [{len(file.content)}]: {repr(file.content)[:150]}")
    print()
