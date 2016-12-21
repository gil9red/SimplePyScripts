#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
В случае неудачной попытки время следующей попытки откладывается на некоторую увеличивающуюся величину.

"""


def work():
    import random
    if random.randint(0, 5):
        raise Exception()

    print('Work!')


timeout = 0.5

# Для обеспечения повторных попыток выполнения используется цикл
while True:
    try:
        work()

        # Если не было исключений, прерываем цикл
        break

    except:
        print('Неудача с таймаутом {}.'.format(timeout))

        import time
        time.sleep(timeout)
        timeout += 0.1

