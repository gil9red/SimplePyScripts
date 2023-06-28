#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from timeit import timeit


projectsIds = {i: 0 if i % 2 == 0 else 1 for i in range(100)}
projects = [{"id": i, "name": str(hex(i))} for i in range(1000)]

NUMBER = 1000

stmt_1 = "list(filter(lambda pr: projectsIds.get(pr['id'], 0), projects))"
stmt_2 = "[pr for pr in projects if projectsIds.get(pr['id'], 0)]"

print(timeit(stmt_1, globals=globals(), number=NUMBER))  # 0.2510618525824858
print(timeit(stmt_2, globals=globals(), number=NUMBER))  # 0.1762350285550252
