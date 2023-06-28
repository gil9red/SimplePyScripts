#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/master/simple_brainfuck.py


def get_loops_block(source):
    begin_block = []
    blocks = dict()

    for i, s in enumerate(source):
        if s is "[":
            begin_block.append(i)

        elif s is "]":
            b_i = begin_block.pop()  # b_i -- begin index
            blocks[i] = b_i
            blocks[b_i] = i

    return blocks


def execute(source, silent=True):
    """
    EN:
    The function parses source code Brainfuck and execute it.

    RU:
    Функция выполняет разбор исходного кода Brainfuck и выполняет его.

    :param source: Исходный код
    :return:
    """

    i = 0  # A pointer to the row index in the code
    x = 0  # Cell index

    from collections import defaultdict

    bf = defaultdict(
        int
    )  # Dictionary, which is stored in the key index of the cell, and in the value - its value
    l = len(source)  # Number of code symbols
    loops_block = get_loops_block(source)

    result_list = []

    while i < l:
        s = source[i]

        if s is ">":  # Go to the next cell
            x += 1

        elif s is "<":  # Go to the previous cell
            x -= 1

        elif s is "+":  # Increasing the value of the current cell on 1
            bf[x] += 1

        elif s is "-":  # Decrease the value of the current cell on 1
            bf[x] -= 1

        elif s is ".":  # Printing the value of the current cell
            value = chr(bf[x])
            result_list.append(value)

            if not silent:
                print(value, end="")

        elif s is ",":  # Enter a value in the current cell
            bf[x] = int(input("Input = "))

        elif s is "[":  # Begin loop
            if not bf[
                x
            ]:  # If bf[x] == 0, then gets the index of the closing parenthesis
                i = loops_block[i]

        elif s is "]":  # End loop
            if bf[x]:  # Если bf[x] != 0, then gets the index of the opening parenthesis
                i = loops_block[i]

        i += 1

    return "".join(result_list)


if __name__ == "__main__":
    text = (
        "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>+++++"
        "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        "+++++++++++++++++.>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        "++++++++++++++++++++++++++++++++++++++++++++++++.>+++++++++++++++++++++++++++++"
        "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        ".>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        "++++++++++++++++++++++++++++++++++.>++++++++++++++++++++++++++++++++.>+++++++++"
        "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++."
        ">++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        "+++++++++++++++++++++++++++++++++.>++++++++++++++++++++++++++++++++++++++++++++"
        "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>+++++++"
        "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        "++++++++++++++++++++++.>+++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        "+++++++++++++++++++++++++++++++++++++++++++++.>+++++++++++++++++++++++++++++++++."
    )
    result = execute(text)
    print("result: " + repr(result))

    text = """
++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++
.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.
------.--------.>+.>.
    """
    result = execute(text)
    print("result: " + repr(result))
