#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import socket
import sys
import time

from threading import Thread

sys.path.append("..")
from common import send_msg, recv_msg


HOST = "127.0.0.1"
PORT = 12002


sock = socket.socket()
sock.connect((HOST, PORT))


# Формат %[2R]L%P
MSG_LEN_FORMAT = ">H"


def read_from() -> None:
    while True:
        response_data: bytes = recv_msg(sock, MSG_LEN_FORMAT)
        if response_data:
            print(f"Response ({len(response_data)}): {response_data.hex()}")
        time.sleep(0.1)


Thread(target=read_from).start()

# Diners Club example
# Заполняется:
#     stan = F11
MESSAGE_TEMPLATE = "31313030F634054000E0A0000000001000000000313630303030303030303030303030303030303130303030303030303030303330303030303030303030303330303030303732343130323832343030{stan}323330373234313632383234353330373630303130303135343130303130303630313076436173685F697069706574726173682D616371202020343169706574726173682D6163712F41647A68697461726F766F2F20202020202020202020202020363433363433363433363433"


stan = 4500
for i in range(20):
    stan_hex = str(stan).encode('ascii').hex()
    message = MESSAGE_TEMPLATE.format(stan=stan_hex)

    data = bytes.fromhex(message)
    print(f"#{i+1}. Sending (stan={stan}): {message}")

    send_msg(sock, data, MSG_LEN_FORMAT)

    stan += 1
    time.sleep(0.1)
