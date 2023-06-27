#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Вашей программе на вход подаются три строки s, a, b, состоящие из строчных латинских букв.
За одну операцию вы можете заменить все вхождения строки a в строку s на строку b.

Например, s = "abab", a = "ab", b = "ba", тогда после выполнения одной операции строка s перейдет в строку "baba",
после выполнения двух и операций – в строку "bbaa", и дальнейшие операции не будут изменять строку s.

Необходимо узнать, после какого минимального количества операций в строке s не останется вхождений строки a, либо же
определить, что это невозможно.

Выведите одно число – минимальное число операций, после применения которых в строке s не останется вхождений строки a.
Если после применения любого числа операций в строке s останутся вхождения строки a, выведите Impossible.

Sample Input 1:
ababa
a
b

Sample Output 1:
1

Sample Input 2:
ababa
b
a

Sample Output 2:
1

Sample Input 3:
ababa
c
c

Sample Output 3:
0

Sample Input 4:
ababac
c
c

Sample Output 4:
Impossible

"""


# Пример использования. В консоли:
# > python main.py < in
# 3


import time


def work(s, a, b):
    t = time.clock()

    count = 0
    while True:
        # Хитрый способ обхода зацикливания, увиденный в комментах.
        # Если функция работает уже больше секунды, прерываем ее и считаем, что решения нет.
        if time.clock() - t > 1:
            print("Impossible")
            return

        if a in s:
            s = s.replace(a, b)
            count += 1
        else:
            break

    print(count)


if __name__ == "__main__":
    s = input()
    a = input()
    b = input()

    work(s, a, b)
