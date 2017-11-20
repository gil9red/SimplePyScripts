#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def makebold(fn):
    def wrapped(*args, **kwargs):
        return "<b>" + fn(*args, **kwargs) + "</b>"

    return wrapped


def makeitalic(fn):
    def wrapped(*args, **kwargs):
        return "<i>" + fn(*args, **kwargs) + "</i>"

    return wrapped


def upper(fn):
    def wrapped(*args, **kwargs):
        return fn(*args, **kwargs).upper()

    return wrapped


@makebold
@makeitalic
@upper
def hello(text):
    return text


print(hello('Hello World!'))  # <b><i>HELLO WORLD!</i></b>
