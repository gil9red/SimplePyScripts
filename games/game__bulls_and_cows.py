#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Быки и коровы

Суть игры: ваш соперник, будь то компьютер или друг, загадывает 4-значное число, состоящее из 
неповторяющихся цифр. Ваша задача — угадать его за ограниченное число ходов. В качестве подсказок 
выступают «коровы» (цифра угадана, но её позиция — нет) и «быки» (когда совпадает и цифра, и её позиция). 
То есть если загадано число «1234», а вы называете «6531», то результатом будет 1 корова (цифра «1») и 
1 бык (цифра «3»). 

"""


import random


def get_unique_four_digits():
    digits = ""

    while len(digits) != 4:
        if len(digits) == 0:
            digit = random.choice("123456789")
        else:
            digit = random.choice("1234567890")

        if digit in digits:
            continue

        digits += digit

    return digits


def get_bulls_and_cows(hidden_num, num):
    bull_count = 0
    cow_count = 0

    for i in range(4):
        if num[i] == hidden_num[i]:
            bull_count += 1

        elif num[i] in hidden_num:
            cow_count += 1

    return bull_count, cow_count


hidden_num = get_unique_four_digits()
print("Я загадал число\n")

trying = 10

while True:
    num = input("Введите 4-х значное число: ")

    # TODO: Удалить
    if num == "show":
        print(hidden_num)
        continue

    # Должно: иметь длину 4, не начинаться на 0, состоять из цифр, и не иметь повторяющихся цифр
    if (
        len(num) != 4
        or num[0] == "0"
        or not num.isdecimal()
        or len(num) != len(set(num))
    ):
        print(f'Неправильный формат числа: "{num}"\n')
        continue

    if num == hidden_num:
        print("Победа!")
        break

    trying -= 1

    if trying == 0:
        print("Закончились попытки. Проигрыш!\nЗагаданное число: " + hidden_num)
        break

    bull_count, cow_count = get_bulls_and_cows(hidden_num, num)
    print(
        f"Быков: {bull_count}, коров: {cow_count}. Осталось попыток: {trying}\n"
    )
