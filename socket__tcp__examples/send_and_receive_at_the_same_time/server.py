#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random
import socket
import time
from threading import Thread

import sys
sys.path.append("..")
from common import send_msg, recv_msg


PORT = 9090


rqs: list[bytes] = []


def write_to() -> None:
    while True:
        if rqs:
            idx = random.randrange(len(rqs))
            data = rqs.pop().upper()
            print(f"Sending #{idx}: {data}")
            send_msg(conn, data)

        time.sleep(0.3)


Thread(target=write_to).start()


while True:
    with socket.socket() as sock:
        sock.bind(("", PORT))
        sock.listen()

        print(f"Server: {sock.getsockname()}")

        while True:
            conn, addr = sock.accept()
            print("Connected:", addr)

            while True:
                try:
                    data = recv_msg(conn)
                    if not data:
                        break

                    print(f"Receiving ({len(data)}): {data}")
                    rqs.append(data)

                except ConnectionResetError:
                    break

            print("Close\n")
