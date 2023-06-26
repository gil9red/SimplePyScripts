#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import socket

import sys
sys.path.append("..")
from common import send_msg, recv_msg


PORT = 9090


with socket.socket() as sock:
    sock.bind(("", PORT))
    sock.listen()

    print(f"Server: {sock.getsockname()}")

    while True:
        conn, addr = sock.accept()
        print("Connected:", addr)

        while True:
            data = recv_msg(conn)
            if not data:
                break

            print(f"Receiving ({len(data)}): {data}")

            print("Sending")
            data = data.decode("utf-8").upper().encode("utf-8")
            send_msg(conn, data)

        print("Close\n")
