#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os

# pip install pygithub
from github import Github

from config import LOGIN, PASSWORD


gh = Github(LOGIN, PASSWORD)
gist = gh.get_gist("2f80a34fb601cd685353")

# Filter by commit version
history_list = [
    x
    for x in gist.history
    if x.version in [
        "d4572ecd5b66ac06a64973cd35ef71936ebf84cd",
        "8040c03f7ee008b0d3ce315a34e4c364f164d939",
        "798e7a89e02cac541e1866ac16278ce9a068cf68",
        "758e49da06e0bb5b6b455e9035a47047ece714d0",
    ]
]

if not os.path.exists("gist_file"):
    os.mkdir("gist_file")

for history in history_list:
    for gist_file_name, gist_file in history.files.items():
        file_name = f"gist_file/{history.version}_{gist_file_name}.txt"

        with open(file_name, mode="w", encoding="utf-8") as f:
            f.write(gist_file.content)
