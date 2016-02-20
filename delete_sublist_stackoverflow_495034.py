#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


# http://ru.stackoverflow.com/questions/495034
# Нужно удалить из списка в вхождения, да не просто по элементам, а прям множество.
# Т.е. если есть список: [0, 1, 2, 3, 1, 5, 3, 7], и например, кортеж, который удаляемых
# элементов (1, 5, 3), нужно, чтобы в итоге получился список [0, 1, 2, 3, 7].
# Как можно легче всего такое реализовать?

l = [0, 1, 2, 3, 1, 5, 3, 7, 1, 5, 3, 8]
m = (1, 5, 3)


def find_sublist(l, m):
    for i in range(len(l)):
        has = False

        try:
            for j in range(len(m)):
                if l[i + j] == m[j]:
                    has = True
                else:
                    has = False
                    break

        except IndexError:
            has = False

        if has:
            yield i, i + len(m)


def delete_sublist(l, m):
    for i, j in find_sublist(l, m):
        del l[i: j]

print('Before: {}.'.format(l))
delete_sublist(l, m)
print('After: {}.'.format(l))
