#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import asyncio
import functools


def makebold(func):
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        return "<b>" + await func(*args, **kwargs) + "</b>"

    return wrapped


def makeitalic(func):
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        return "<i>" + await func(*args, **kwargs) + "</i>"

    return wrapped


def upper(func):
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        return (await func(*args, **kwargs)).upper()

    return wrapped


@makebold
@makeitalic
@upper
async def hello(text):
    return text


loop = asyncio.new_event_loop()

print(loop.run_until_complete(hello("Hello World!")))
# <b><i>HELLO WORLD!</i></b>

assert loop.run_until_complete(hello("Hello World!")) == "<b><i>HELLO WORLD!</i></b>"
