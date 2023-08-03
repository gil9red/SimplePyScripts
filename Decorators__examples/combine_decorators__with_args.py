#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import functools


def get_attrs_str(kwargs: dict) -> str:
    attrs = ""
    if kwargs:
        attrs = " " + " ".join(f'{k}="{v}"' for k, v in kwargs.items())

    return attrs


def makebold(**decorator_kwargs):
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            attrs = get_attrs_str(decorator_kwargs)
            return f"<b{attrs}>{func(*args, **kwargs)}</b>"

        return wrapped

    return actual_decorator


def makeitalic(**decorator_kwargs):
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            attrs = get_attrs_str(decorator_kwargs)
            return f"<i{attrs}>{func(*args, **kwargs)}</i>"

        return wrapped

    return actual_decorator


def upper(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs).upper()

    return wrapped


def custom_tag(
    name: str,
    **arguments,
):
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            attrs = get_attrs_str(arguments)
            return f"<{name}{attrs}>{func(*args, **kwargs)}</{name}>"

        return wrapped

    return actual_decorator


def composed(*decs):
    def deco(f):
        for dec in reversed(decs):
            f = dec(f)
        return f

    return deco


def multi(func):
    return composed(
        custom_tag(
            name="a",
            href="https://example.com",
            title="Hint!",
        ),
        makebold(foo="1"),
        makeitalic(bar="2"),
        upper,
    )(func)


@custom_tag(
    name="a",
    href="https://example.com",
    title="Hint!",
)
@makebold(foo="1")
@makeitalic(bar="2")
@upper
def hello(text):
    return text


@multi
def hello_2(text):
    return text


if __name__ == '__main__':
    print(hello("Hello World!"))
    # <a href="https://example.com" title="Hint!"><b foo="1"><i bar="2">HELLO WORLD!</i></b></a>

    print(hello_2("Hello World!"))
    # <a href="https://example.com" title="Hint!"><b foo="1"><i bar="2">HELLO WORLD!</i></b></a>
