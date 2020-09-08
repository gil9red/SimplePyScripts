#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import functools


def get_attrs_str(kwargs: dict) -> str:
    attrs = ''
    if kwargs:
        attrs = ' ' + ' '.join(f'{k}="{v}"' for k, v in kwargs.items())

    return attrs


def makebold(**decorator_kwargs):
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            attrs = get_attrs_str(decorator_kwargs)
            return f"<b{attrs}>" + func(*args, **kwargs) + "</b>"

        return wrapped

    return actual_decorator


def makeitalic(**decorator_kwargs):
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            attrs = get_attrs_str(decorator_kwargs)
            return f"<i{attrs}>" + func(*args, **kwargs) + "</i>"

        return wrapped

    return actual_decorator


def upper(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs).upper()

    return wrapped


def composed(*decs):
    def deco(f):
        for dec in reversed(decs):
            f = dec(f)
        return f
    return deco


def multi(func):
    return composed(
        makebold(foo="1"),
        makeitalic(bar="2"),
        upper,
    )(func)


@makebold(foo="1")
@makeitalic(bar="2")
@upper
def hello(text):
    return text


@multi
def hello_2(text):
    return text


print(hello('Hello World!'))
# <b foo="1"><i bar="2">HELLO WORLD!</i></b>

print(hello_2('Hello World!'))
# <b foo="1"><i bar="2">HELLO WORLD!</i></b>
