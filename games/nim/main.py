#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random


class FinishGameException(Exception):
    pass


MIN_STONES: int = 1
MAX_STONES: int = 3
MAX_NUMBER: int = 21

gamer_is_first: bool = (input("Ты первый? (y/n): ").lower() or "y") == "y"
number: int = MAX_NUMBER


def player_move():
    global number

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
        raise FinishGameException("Компьютер выиграл")


def computer_move():
    global number

    # TODO: Когда остается минимум камней нужно вручную выбрать правильное, а не рандомно
    #       А то ИИ выглядит как искусственный идиот
    stones = min(number, random.randint(MIN_STONES, MAX_STONES))
    print(f"Компьютер выбрал: {stones}")
    number -= stones
    if number <= 0:
        raise FinishGameException("Ты выиграл")


while number > 0:
    print(f"Камней: {number}")

    try:
        if gamer_is_first:
            player_move()
            computer_move()
        else:
            computer_move()
            player_move()

    except FinishGameException as e:
        print(e)

    print()
