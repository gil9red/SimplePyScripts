#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install github3.py
from github3 import GitHub

from config import TOKEN


g = GitHub(token=TOKEN)

gist = g.gist('2f80a34fb601cd685353')

for commit in gist.commits():
    print(commit.committed_at, commit.version, len(commit.gist().files['gistfile1.txt'].content()))
