#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import asyncio

# pip install aiohttp
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://python.org') as rs:
            print("Status:", rs.status)
            print("Content-type:", rs.headers['content-type'])

            html = await rs.text()
            print("Body:", html[:15], "...")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
