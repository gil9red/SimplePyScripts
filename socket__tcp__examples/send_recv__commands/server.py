#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as DT
import random
import socket
import sys

sys.path.append("..")
from common import send_msg, recv_msg


PORT = 9090


def execute_command(command: str) -> str:
    if command == "CURRENT_DATETIME":
        return DT.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    elif command == "CURRENT_TIMESTAMP":
        return str(DT.datetime.now().timestamp())

    elif command == "RANDOM":
        return str(random.randint(0, 1000000))

    elif command == "EXIT":
        return "OK"

    else:
        return '<UNKNOWN COMMAND: "{}">'.format(command)


with socket.socket() as sock:
    sock.bind(("", PORT))
    sock.listen()

    print("Server: {}".format(sock.getsockname()))

    while True:
        conn, addr = sock.accept()
        print("Connected:", addr)

        data = recv_msg(conn)
        print("Receiving ({}): {}".format(len(data), data))

        command = str(data, "utf-8")
        response_data = execute_command(command)
        response_data = bytes(response_data, "utf-8")

        print("Sending")
        send_msg(conn, response_data)

        if command == "EXIT":
            sys.exit()

        print("Close\n")
