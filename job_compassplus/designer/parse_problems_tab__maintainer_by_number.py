#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import PATH_PROBLEMS_TAB, parse_text


text = PATH_PROBLEMS_TAB.read_text("utf-8")

# TODO:
filter_by_codes: list[int] = [
    # 127, 137
]

user_by_number: dict[str, int] = dict()

for p in parse_text(text):
    if filter_by_codes and p.code not in filter_by_codes:
        continue

    users = p.maintainers.copy()
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
