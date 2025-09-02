#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random

# TODO: Возможность выбрать кто первый ходит

MIN_STONES: int = 1
MAX_STONES: int = 3
MAX_NUMBER: int = 21

number: int = MAX_NUMBER
while number > 0:
    print(f"Камней: {number}")

    while True:
        try:
            stones = int(input(f"Камни от {MIN_STONES} до {MAX_STONES}: "))
            assert MIN_STONES <= stones <= MAX_STONES
            break
        except:
            print("Неправильное значение!")
            continue

    number -= stones
    if number <= 0:
        print("Компьютер выиграл")
        break

    # TODO: Когда остается минимум камней нужно вручную выбрать правильное, а не рандомно
    #       А то ИИ выглядит как искусственный идиот
    stones = min(number, random.randint(MIN_STONES, MAX_STONES))
    print(f"Компьютер выбрал: {stones}")
    number -= stones
    if number <= 0:
        print("Ты выиграл")
        break

    print()
