#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from timeit import timeit


y = [
    348,
    336,
    330,
    340,
    332,
    333,
    344,
    348,
    349,
    354,
    375,
    379,
    365,
    356,
    341,
    312,
    300,
    294,
    304,
    323,
]
test_globals = dict(y=y)

t = timeit("x = list(range(len(y)))", globals=test_globals)
print(f"Elapsed: {t:.3f} secs")

t = timeit("x = [i for i in range(len(y))]", globals=test_globals)
print(f"Elapsed: {t:.3f} secs")

t = timeit(
    """
x = []
for i in range(len(y)):
    x.append(i)
""",
    globals=test_globals,
)
print(f"Elapsed: {t:.3f} secs")

t = timeit(
    """
x = list()
for i in range(len(y)):
    x.append(i)
""",
    globals=test_globals,
)
print(f"Elapsed: {t:.3f} secs")

"""
Elapsed: 0.542 secs
Elapsed: 0.966 secs
Elapsed: 1.530 secs
Elapsed: 1.607 secs
"""
