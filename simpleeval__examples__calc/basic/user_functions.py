#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/danthedeckie/simpleeval#functions


# Default functions (simpleeval.DEFAULT_FUNCTIONS):
# +------------+---------------------------------------+
# | randint(x) | Return a random int below x           |
# +------------+---------------------------------------+
# | rand()     | Return a random float between 0 and 1 |
# +------------+---------------------------------------+
# | int(x)     | Convert x to an int.                  |
# +------------+---------------------------------------+
# | float(x)   | Convert x to a float.                 |
# +------------+---------------------------------------+
# | str(x)     | Convert x to a str (unicode in py2)   |
# +------------+---------------------------------------+


# pip install simpleeval
from simpleeval import simple_eval, DEFAULT_FUNCTIONS


print(simple_eval("square(11)", functions={"square": lambda x: x * x}))  # 11
print(simple_eval("double(21)", functions={"double": lambda x: x * 2}))  # 42
print(simple_eval("my_pow(11, 2)", functions={"my_pow": lambda a, b: a**b}))  # 121
print()


def double(x):
    return x * 2


my_functions = {"d": double, "double": double}
print(simple_eval("d(100) + double(1)", functions=my_functions))  # 202


my_functions = DEFAULT_FUNCTIONS.copy()
my_functions.update(
    square=lambda x: x * x,
    double=lambda x: x * 2,
)
print(simple_eval("square(randint(100))", functions=my_functions))  # 1024
