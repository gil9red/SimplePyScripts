#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import socket

import sys
sys.path.append("..")
from common import send_msg, recv_msg


HOST, PORT = "localhost", 9090


def send_command(command: str) -> str:
    with socket.socket() as sock:
        sock.connect((HOST, PORT))

        data = bytes(command, "utf-8")
        send_msg(sock, data)

        response_data = recv_msg(sock)
        return str(response_data, "utf-8")


if __name__ == "__main__":
    rs = send_command("CURRENT_DATETIME")
    print(rs)

    rs = send_command("CURRENT_TIMESTAMP")
    print(rs)

    rs = send_command("RANDOM")
    print(rs)

    rs = send_command("FOO_BAR")
    print(rs)

    rs = send_command("EXIT")
    print(rs)
