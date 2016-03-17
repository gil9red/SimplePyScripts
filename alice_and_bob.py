#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# «Если Алиса будет кидать монетки до тех пор, пока не получит решку, следующую за орлом, а Боб – до тех пор,
# пока не получит две решки подряд, то Алисе в среднем потребуется четыре броска монеты, в то время как Бобу – шесть.»

from random import randrange

RESHKA = 0
OREL = 1


def alice():
    curr = randrange(2)
    last = randrange(2)
    count = 2

    if curr == RESHKA and last == OREL:
        return 2

    while True:
        curr = randrange(2)
        if curr == RESHKA and last == OREL:
            break

        last = curr
        count += 1

    return count


def bob():
    curr = randrange(2)
    last = randrange(2)
    count = 2

    if curr == RESHKA and last == RESHKA:
        return 2

    while True:
        curr = randrange(2)
        if curr == RESHKA and last == RESHKA:
            break

        last = curr
        count += 1

    return count


COUNT = 10000

print(sum([alice() for _ in range(COUNT)]) // COUNT)
print(sum([bob() for _ in range(COUNT)]) // COUNT)
