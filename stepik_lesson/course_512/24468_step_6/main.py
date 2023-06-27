#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Лямбда функции предоставляют нам удобный способ создать функцию «прямо на месте».
Но иногда, когда нужно создавать много однотипных лямбда функций, еще удобнее будет создать функцию,
которая будет их генерировать.

Реализуйте функцию mod_checker(x, mod=0), которая будет генерировать лямбда функцию от одного аргумента y,
которая будет возвращать True, если остаток от деления y на x равен mod, и False иначе.

Пример использования:
mod_3 = mod_checker(3)

print(mod_3(3)) # True
print(mod_3(4)) # False

mod_3_1 = mod_checker(3, 1)
print(mod_3_1(4)) # True

"""


def mod_checker(x, mod=0):
    return lambda y: y % x == mod


if __name__ == "__main__":
    mod_3 = mod_checker(3)

    print(mod_3(3))  # True
    print(mod_3(4))  # False

    mod_3_1 = mod_checker(3, 1)
    print(mod_3_1(4))  # True
