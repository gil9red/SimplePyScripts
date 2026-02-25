#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/aio-libs/aiohttp


# pip install aiohttp
import aiohttp
import asyncio

from lxml import etree


async def fetch(session, url):
    async with session.get(url) as response:
        # Возвращаем ответ в байтах
        return await response.content.read()


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        xml_str = await fetch(session, "https://sdvk-oboi.ru/sitemap.xml")
        root = etree.fromstring(xml_str)

        for url in root.xpath('//*[local-name()="loc"]/text()'):
            print(url)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
