#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
В случае неудачной попытки время следующей попытки откладывается на некоторую увеличивающуюся величину.

"""


import random
import time


def work():
    if random.randint(0, 5):
        raise Exception()

    print("Work!")


timeout = 0.5

# Для обеспечения повторных попыток выполнения используется цикл
while True:
    try:
        work()

        # Если не было исключений, прерываем цикл
        break

    except:
        print(f"Неудача с таймаутом {timeout}.")

        time.sleep(timeout)
        timeout += 0.1
