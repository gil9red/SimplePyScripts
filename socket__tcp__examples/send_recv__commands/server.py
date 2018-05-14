#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import socket

import sys
sys.path.append('..')

from common import send_msg, recv_msg


PORT = 9090


def execute_command(command: str) -> str:
    if command == 'CURRENT_DATETIME':
        import datetime as DT
        return DT.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    elif command == 'CURRENT_TIMESTAMP':
        import datetime as DT
        return str(DT.datetime.now().timestamp())

    elif command == 'RANDOM':
        import random
        return str(random.randint(0, 1000000))

    else:
        return '<UNKNOWN COMMAND: "{}">'.format(command)


with socket.socket() as sock:
    sock.bind(('', 9090))
    sock.listen(1)

    print('Server: {}'.format(sock.getsockname()))

    while True:
        conn, addr = sock.accept()
        print('Connected:', addr)

        data = recv_msg(conn)
        print('Receiving: {}: {}'.format(len(data), data))

        command = str(data, 'utf-8')
        response_data = execute_command(command)
        response_data = bytes(response_data, 'utf-8')

        print('Sending')
        send_msg(conn, response_data)

        print('Close\n')
