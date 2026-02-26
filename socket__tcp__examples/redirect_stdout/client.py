#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import contextlib
import socket
import sys

sys.path.append("..")
from common import send_msg, recv_msg


HOST, PORT = "localhost", 9090


class SocketIO:
    def __init__(self, socket: socket.socket) -> None:
        self.socket = socket

    def write(self, text: str) -> None:
        data = text.encode("utf-8")
        print(f"Sending ({len(data)}): {data!r}", file=sys.stderr)

        send_msg(self.socket, data)

        response_data = recv_msg(self.socket)
        if response_data:
            print(
                f"Response ({len(response_data)}): {response_data!r}", file=sys.stderr
            )


sock = socket.socket()
sock.connect((HOST, PORT))

f = SocketIO(sock)
with contextlib.redirect_stdout(f):
    print("123")
    print("Hello World!")
    print("Привет мир!")

    for i in range(1, 5 + 1):
        print(f"{i} * {i} = {i * i}")
