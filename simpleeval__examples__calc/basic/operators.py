#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/danthedeckie/simpleeval#operators


# You can add operators yourself, using the operators argument, but these are the defaults:
# +----+---------------------------------------------------------------------------------+
# | +  | add two things. x + y 1 + 1 -> 2                                                |
# +----+---------------------------------------------------------------------------------+
# | -  | subtract two things x - y 100 - 1 -> 99                                         |
# +----+---------------------------------------------------------------------------------+
# | /  | divide one thing by another x / y 2/3 -> 0.6666666666666666                     |
# +----+---------------------------------------------------------------------------------+
# | // | divide one thing by another x // y 2//3 -> 0                                    |
# +----+---------------------------------------------------------------------------------+
# | *  | multiple one thing by another x * y 10 * 10 -> 100                              |
# +----+---------------------------------------------------------------------------------+
# | ** | 'to the power of' x**y 2 ** 10 -> 1024                                          |
# +----+---------------------------------------------------------------------------------+
# | %  | modulus. (remainder) x % y 15 % 4 -> 3                                          |
# +----+---------------------------------------------------------------------------------+
# | == | equals x == y 15 == 4 -> False                                                  |
# +----+---------------------------------------------------------------------------------+
# | != | not equals x != y 15 != 4 -> True                                               |
# +----+---------------------------------------------------------------------------------+
# | <  | Less than. x < y 1 < 4 -> True                                                  |
# +----+---------------------------------------------------------------------------------+
# | >  | Greater than. x > y 1 > 4 -> False                                              |
# +----+---------------------------------------------------------------------------------+
# | <= | Less than or Equal to. x <= y 1 <= 4 -> True                                    |
# +----+---------------------------------------------------------------------------------+
# | >= | Greater or Equal to x >= 21 1 >= 4 -> False                                     |
# +----+---------------------------------------------------------------------------------+
# | in | is something contained within something else. "spam" in "my breakfast" -> False |
# +----+---------------------------------------------------------------------------------+


# pip install simpleeval
from simpleeval import simple_eval


print(simple_eval("21 + 21"))  # 42
print(simple_eval("100 - 1"))  # 99
print(simple_eval("2 / 3"))  # 0.6666666666666666
print(simple_eval("2 // 3"))  # 0
print(simple_eval("10 * 10"))  # 100
print(simple_eval("2 ** 10"))  # 1024
print(simple_eval("15 % 4"))  # 3
print()
print(simple_eval("15 == 4"))  # False
print(simple_eval("15 != 4"))  # True
print(simple_eval("1 < 4"))  # True
print(simple_eval("1 > 4"))  # False
print(simple_eval("1 <= 4"))  # True
print(simple_eval("1 >= 4"))  # False
print()
print(simple_eval("'ell' in 'Hello'"))  # True
print(simple_eval("'123' in 'ab123c'"))  # True
print(simple_eval("'ell' not in 'Hello'"))  # False
