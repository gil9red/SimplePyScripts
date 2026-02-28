#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "ipetrash"


# http://ru.stackoverflow.com/questions/495034
# Нужно удалить из списка в вхождения, да не просто по элементам, а прям множество.
# Т.е. если есть список: [0, 1, 2, 3, 1, 5, 3, 7], и например, кортеж, который удаляемых
# элементов (1, 5, 3), нужно, чтобы в итоге получился список [0, 1, 2, 3, 7].
# Как можно легче всего такое реализовать?

l = [0, 1, 2, 3, 1, 5, 3, 7, 1, 5, 3, 8]
m = (1, 5, 3)


def find_sublist(l, m):
    for i in range(len(l)):
        try:
            if tuple(l[i : i + len(m)]) == tuple(m):
                yield i, i + len(m)

        except IndexError:
            pass


def delete_sublist(l, m) -> None:
    for i, j in find_sublist(l, m):
        del l[i:j]


print(f"Before: {l}.")
delete_sublist(l, m)
print(f"After: {l}.")
