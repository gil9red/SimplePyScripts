#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import socket

from bs4 import BeautifulSoup

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

        xml_data = BeautifulSoup(data, "html.parser")
        print("xml_data:", xml_data)

        xml_data.title.string = "updates"
        xml_data.counter.string = str(int(xml_data.counter.text) + 1)

        data = str(xml_data)
        print("Sending: {}".format(data))

        rs = bytes(data, "utf-8")
        send_msg(conn, rs)

        print("Close\n")
