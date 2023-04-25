#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Very-very simple calc
def calc(expr):
    operator_function = {
        "-": lambda x, y: x - y,
        "+": lambda x, y: x + y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y,
    }

    nums = list()
    opers = list()

    tokens = list("(" + expr + ")")

    while tokens:
        token = tokens.pop(0)

        if token.isdecimal():
            nums.append(float(token))
        else:
            if token == ")":
                oper = opers.pop()
                while opers and oper != "(":
                    b, a = nums.pop(), nums.pop()
                    f = operator_function[oper]
                    nums.append(f(a, b))

                    oper = opers.pop()

            else:
                opers.append(token)

    return nums[0]


if __name__ == "__main__":
    print(calc("((1+(2*3))*2)+4"))  # 18.0
    print(calc("(1*(3/2))+4"))  # 5.5
    print(calc("(2*(3/2))+4"))  # 7.0
