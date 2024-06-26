#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import socket

import sys
sys.path.append("..")
from common import send_msg__with_crc32, recv_msg__with_crc32


PORT = 9090


with socket.socket() as sock:
    sock.bind(("", PORT))
    sock.listen()

    print(f"Server: {sock.getsockname()}")

    while True:
        conn, addr = sock.accept()
        print("Connected:", addr)

        data = recv_msg__with_crc32(conn)
        print(f"Receiving ({len(data)}): {data}")

        text = f"Ok! Message size: {len(data)}"
        print(f"Sending: {text}")

        rs = bytes(text, "utf-8")
        send_msg__with_crc32(conn, rs)

        print("Close\n")
