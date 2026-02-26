#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from textwrap import dedent


text = """\
    Съешь ещё этих мягких французских 
    булок, да выпей же чаю
"""
print(repr(text))
print(repr(dedent(text)))

print()


def foo() -> None:
    """
    Съешь ещё этих мягких французских
    булок, да выпей же чаю
    """


print(repr(foo.__doc__))
print(repr(dedent(foo.__doc__)))
