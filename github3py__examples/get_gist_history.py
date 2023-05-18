#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/sigmavirus24/github3.py


# pip install github3.py
from github3 import GitHub

from config import TOKEN


gh = GitHub(token=TOKEN)

gist = gh.gist("2f80a34fb601cd685353")

for commit in gist.commits():
    # TODO: KeyError: 'gistfile1.txt'
    print(
        commit.committed_at,
        commit.version,
        len(commit.gist().files["gistfile1.txt"].content()),
    )
