#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# «Если Алиса будет кидать монетки до тех пор, пока не получит решку, следующую за орлом, а Боб – до тех пор,
# пока не получит две решки подряд, то Алисе в среднем потребуется четыре броска монеты, в то время как Бобу – шесть.»


from random import randrange


def alice():
    curr, last = None, None
    count = 0

    while True:
        last = curr
        curr = randrange(2)
        count += 1

        if curr == 0 and last == 1:
            break

    return count


def bob():
    curr, last = None, None
    count = 0

    while True:
        last = curr
        curr = randrange(2)
        count += 1

        if curr == 0 and last == 0:
            break

    return count


COUNT = 10000

print(sum([alice() for _ in range(COUNT)]) // COUNT)
print(sum([bob() for _ in range(COUNT)]) // COUNT)
