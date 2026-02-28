#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/aaugustin/websockets


import asyncio

# pip install websockets
import websockets


async def hello(url: str) -> None:
    async with websockets.connect(url) as websocket:
        await websocket.send("Hello World!")

        print(await websocket.recv())
        # Hello World!


if __name__ == "__main__":
    # From http://websocket.org/echo.html
    url = "wss://echo.websocket.org"

    asyncio.get_event_loop().run_until_complete(hello(url))
