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

    print("Server: {}".format(sock.getsockname()))

    while True:
        conn, addr = sock.accept()
        print("Connected:", addr)

        data = recv_msg(conn)
        print("Receiving ({}): {}".format(len(data), data))

        text = "Ok! Message size: {}".format(len(data))
        print("Sending: {}".format(text))

        rs = bytes(text, "utf-8")
        send_msg(conn, rs)

        print("Close\n")
