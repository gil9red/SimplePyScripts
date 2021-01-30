#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import asyncio

# pip install aiohttp
import aiohttp

from ignore_aiohttp_ssl_error import ignore_aiohttp_ssl_error


async def fetch_page(url: str, idx: int):
    async with aiohttp.request("GET", url) as rs:
        if rs.status == 200:
            print(f"[{idx}] Data fetched successfully")
        else:
            print(f"[{idx}] Data fetch failed, HTTP status = {rs.status}")
            print(rs.content)


async def main():
    url = 'https://python.org'
    urls = [url] * 100

    tasks = [
        asyncio.create_task(fetch_page(url, idx))
        for idx, url in enumerate(urls, 1)
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    import time
    t = time.perf_counter()

    loop = asyncio.get_event_loop()
    ignore_aiohttp_ssl_error(loop)
    loop.run_until_complete(main())

    print(f'Elapsed {time.perf_counter() - t:.2f} secs')
