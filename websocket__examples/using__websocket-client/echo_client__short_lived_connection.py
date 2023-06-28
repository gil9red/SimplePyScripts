#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/websocket-client/websocket-client#short-lived-one-off-send-receive


# pip install websocket-client
import websocket


# From http://websocket.org/echo.html
url = "wss://echo.websocket.org"

ws = websocket.create_connection(url)

text = "Hello, World!"
print(f"[#] Sending '{text!r}'...")
ws.send(text)
print("[#] Sent")
print("[#] Receiving...")
result = ws.recv()
print(f"[#] Received: {result!r}")
# [#] Received: 'Hello, World!'

text = "Привет мир!"
print(f"[#] Sending '{text!r}'...")
ws.send(text)
print("[#] Sent")
print("[#] Receiving...")
result = ws.recv()
print(f"[#] Received: {result!r}")
# [#] Received: 'Привет мир!'

ws.close()
