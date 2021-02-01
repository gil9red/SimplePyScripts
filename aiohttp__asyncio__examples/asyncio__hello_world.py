#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import asyncio


async def main():
    print('Hello ', end='')
    await asyncio.sleep(1)
    print('World!')


# Python 3.7+
asyncio.run(main())
# Hello World!
