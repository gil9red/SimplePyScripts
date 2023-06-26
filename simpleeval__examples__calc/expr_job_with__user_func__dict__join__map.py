#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install simpleeval
from simpleeval import simple_eval, SimpleEval


my_functions = {
    "my_pos": lambda: {"x": 12, "y": 10},
    "map": map,
    "str": str,
}

print(simple_eval('my_pos()["x"] * my_pos()["y"]', functions=my_functions))  # 120
print(
    simple_eval('"x".join(map(str, my_pos().values()))', functions=my_functions)
)
# 12x10
print()

# OR:
my_eval = SimpleEval(functions=my_functions)

print(my_eval.eval('my_pos()["x"] * my_pos()["y"]'))  # 120
print(my_eval.eval('"x".join(map(str, my_pos().values()))'))  # 12x10
