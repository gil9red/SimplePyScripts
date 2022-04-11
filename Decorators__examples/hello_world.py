#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import functools


def makebold(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        return "<b>" + func(*args, **kwargs) + "</b>"

    return wrapped


def makeitalic(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        return "<i>" + func(*args, **kwargs) + "</i>"

    return wrapped


def upper(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs).upper()

    return wrapped


@makebold
@makeitalic
@upper
def hello(text):
    return text


print(hello('Hello World!'))
# <b><i>HELLO WORLD!</i></b>

assert hello('Hello World!') == '<b><i>HELLO WORLD!</i></b>'
