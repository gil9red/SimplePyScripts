#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Вашей программе на вход подаются две строки s и t, состоящие из строчных латинских букв.
Выведите одно число – количество вхождений строки t в строку s.

Пример:
s = "abababa"
t = "aba"


Sample Input 1:
abababa
aba

Sample Output 1:
3

Sample Input 2:
abababa
abc

Sample Output 2:
0

Sample Input 3:
abc
abc

Sample Output 3:
1

Sample Input 4:
aaaaa
a

Sample Output 4:
5
"""


# Пример использования. В консоли:
# > python main.py < in
# 3


def count_sub_string(s, t):
    """Функция подсчитывает и возвращает количество вхождений строки t в строку s."""

    count = 0
    for i in range(len(s)):
        part = s[i : i + len(t)]
        if not part:
            break

        if t == part:
            count += 1

    return count


if __name__ == "__main__":
    s = input()
    t = input()

    print(count_sub_string(s, t))
