#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def draw_handman(number_wrong_answer, max_wrong_answer=5):
    if number_wrong_answer == 0:
        return ""

    handman_text = """\
    ____
    | |
    | \O/
    |  |
    | / \\
    ___|___ """

    if number_wrong_answer >= max_wrong_answer:
        return handman_text

    part = int(max_wrong_answer / number_wrong_answer)
    return "\n".join(handman_text.split("\n")[: max_wrong_answer - part + 1])


if __name__ == "__main__":
    print(draw_handman(0))
    print("-" * 15)
    print(draw_handman(1))
    print("-" * 15)
    print(draw_handman(2))
    print("-" * 15)
    print(draw_handman(3))
    print("-" * 15)
    print(draw_handman(4))
    print("-" * 15)
    print(draw_handman(5))
