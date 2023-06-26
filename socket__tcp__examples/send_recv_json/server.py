#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
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

        data = recv_msg(conn)
        print(f"Receiving ({len(data)}): {data}")

        json_data = json.loads(data, encoding="utf-8")
        print("json_data:", json_data)

        json_data["title"] = "updates"
        json_data["counter"] += 1

        data = json.dumps(json_data)
        print(f"Sending: {data}")

        rs = bytes(data, "utf-8")
        send_msg(conn, rs)

        print("Close\n")
