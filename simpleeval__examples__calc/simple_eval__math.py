#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import math
import inspect

# pip install simpleeval
from simpleeval import SimpleEval


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/6c512c0e0df249822ff0f46bc32faaf4f74d6e05/get_functions_from_object__module_class_object.py
def get_name_by_func(obj: object) -> dict:
    is_ok = lambda name, func: inspect.isroutine(func) and not name.startswith("_")

    return {name: func for name, func in inspect.getmembers(obj) if is_ok(name, func)}


class SimpleMathEval(SimpleEval):
    def __init__(self):
        names = {
            "e": math.e,
            "inf": math.inf,
            "nan": math.nan,
            "pi": math.pi,
            "tau": math.tau,
            "True": True,
            "False": False,
        }
        functions = get_name_by_func(math)

        super().__init__(names=names, functions=functions)


if __name__ == "__main__":
    math_eval = SimpleMathEval()

    print(math_eval.eval("pi ** 2"))  # 9.869604401089358
    print(math_eval.eval("pow(4, 2)"))  # 16
    print(math_eval.eval("4 ** 2"))  # 16
    print(math_eval.eval("log(10)"))  # 2.302585092994046
    print()

    print(math_eval.eval("sin(4) ** 2 + cos(4) ** 2"))  # 1.0
    print(math_eval.eval("sin(4) ** 2 + cos(4) ** 2 == 1"))  # True
    print()

    print(math_eval.eval("factorial(5)"))  # 120
    print(math_eval.eval("gcd(9, 3)"))  # 3
    print()

    print(math_eval.eval("inf + 2"))  # inf
    print(math_eval.eval("inf + inf"))  # inf
    print()

    print(math_eval.eval("nan + 2"))  # nan
    print(math_eval.eval("nan + nan"))  # nan
    print(math_eval.eval("nan + inf"))  # nan
    print()
