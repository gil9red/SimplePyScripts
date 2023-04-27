#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.wikibooks.org/wiki/Реализации_алгоритмов/Расстояние_Левенштейна#Python
def distance(a, b):
    """Calculates the Levenshtein distance between a and b."""

    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)  # Keep current and previous row, not entire matrix
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = (
                previous_row[j] + 1,
                current_row[j - 1] + 1,
                previous_row[j - 1],
            )
            if a[j - 1] != b[i - 1]:
                change += 1

            current_row[j] = min(add, delete, change)

    return current_row[n]


if __name__ == "__main__":
    print(distance("Привет", "Превет"))  # 1
    print(distance("Привет", "Првет"))   # 1
    print(distance("Привет", "Првед"))   # 2
