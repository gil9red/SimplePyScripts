#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from pathlib import Path


text = (Path(__file__).parent / "problems_tab.txt").read_text("utf-8")

user_by_number: dict[str, int] = dict()
for line in text.strip().splitlines():
    if not line.startswith("*"):
        continue

    users = []
    for brackets in re.findall(r"\[(.*?)]", line):
        if "@" in brackets:
            emails = brackets.split(", ")
            users += [email.split("@")[0] for email in emails]

    if not users:
        users.append("<unknown>")

    for user in users:
        if user not in user_by_number:
            user_by_number[user] = 0
        user_by_number[user] += 1

print(f"Users ({len(user_by_number)}):")
for user, number in sorted(user_by_number.items(), key=lambda x: x[1], reverse=True):
    print(f"  {user!r}: {number}")
"""
Users (3):
  'bar': 7
  'foo': 3
  '<unknown>': 2
"""
