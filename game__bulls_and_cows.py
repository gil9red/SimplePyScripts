#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import random


def get_unique_four_digits():
    digits = ''

    while len(digits) != 4:
        if len(digits) == 0:
            digit = random.choice('123456789')
        else:
            digit = random.choice('1234567890')

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
print('Я загадал число\n')

trying = 2

while True:
    num = input('Введите 4-х значное число: ')

    # TODO: Удалить
    if num == '9999':
        print(hidden_num)
        continue

    # Должно: иметь длину 4, не начинаться не на 0, состоять из цифр, и не иметь повторяющихся цифр
    if len(num) != 4 or num[0] == '0' or not num.isdecimal() or len(num) != len(set(num)):
        print('Неправильный формат числа: "{}"\n'.format(num))
        continue

    if num == hidden_num:
        print('Победа!')
        break

    trying -= 1

    if trying == 0:
        print('Закончились попытки. Проирыш!\nЗагаданное число: ' + hidden_num)
        break

    bull_count, cow_count = get_bulls_and_cows(hidden_num, num)
    print('Быков: {}, коров: {}. Осталось попыток: {}\n'.format(bull_count, cow_count, trying))
