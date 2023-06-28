#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/websocket-client/websocket-client#short-lived-one-off-send-receive


# pip install websocket-client
import websocket


websocket.enableTrace(True)

# From http://websocket.org/echo.html
url = "wss://echo.websocket.org"

ws = websocket.create_connection(url)

ws.send("Hello, World")
result = ws.recv()
print(f"[#] Received: {result!r}")
# [#] Received: 'Hello, World'

ws.send("Привет мир!")
result = ws.recv()
print(f"[#] Received: {result!r}")
# [#] Received: 'Привет мир!'

ws.close()
