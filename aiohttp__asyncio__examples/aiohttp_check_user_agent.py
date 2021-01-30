#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import asyncio

# pip install aiohttp
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://httpbin.org/get') as rs:
            print("Status:", rs.status)
            print("Content-type:", rs.headers['content-type'])

            data = await rs.json()
            print(data['headers']['User-Agent'])
            # Python/3.7 aiohttp/3.7.3


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
