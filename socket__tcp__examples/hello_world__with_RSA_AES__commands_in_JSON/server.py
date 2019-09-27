#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from base64 import b64decode, b64encode
import json
import secrets
import socket
import threading

import sys
sys.path.append('..')

from common import send_msg, recv_msg
from utils import CommandEnum
import rsa


CONNECTION_BY_KEY = dict()


def process_command(data: bytes, conn, addr) -> bytes:
    rq = json.loads(data, encoding='utf-8')

    command = CommandEnum[rq['command']]

    if command == CommandEnum.NEW_PUBLIC_KEY:
        # Публичный ключ от клиента
        public_key = rsa.import_key(rq['data'])

        # Придумываем ключ для шифрования сообщений
        key_AES = secrets.token_bytes(32)
        print('key_AES:', key_AES)
        CONNECTION_BY_KEY[conn] = key_AES

        # Шифруем ключ сообщений публичным ключом клиента
        encrypted = b64encode(rsa.encrypt(key_AES, public_key)).decode('utf-8')
        rq['data'] = encrypted

    # TODO: more commands

    else:
        rq['data'] = f'<Unsupported command="{command}">'

    return json.dumps(rq, ensure_ascii=False).encode('utf-8')


def process_connect(conn, addr):
    print(f"New connection from {addr}")

    try:
        while True:
            data = recv_msg(conn)
            if not data:
                break

            print(f'Receiving ({len(data)}): {data}')

            rs = process_command(data, conn, addr)

            print(f'Sending ({len(rs)}): {rs}')
            send_msg(conn, rs)

    except:
        import traceback
        print(traceback.format_exc())

    finally:
        conn.close()

        if conn in CONNECTION_BY_KEY:
            CONNECTION_BY_KEY.pop(conn)

        print(f"Closed connection from {addr}")
        print()


HOST, PORT = '', 9090


with socket.socket() as sock:
    print('Server created')

    sock.bind((HOST, PORT))
    print('Server bind complete')

    sock.listen()
    print(f'Server now listening: {sock.getsockname()}')
    print()

    while True:
        conn, addr = sock.accept()

        thread = threading.Thread(target=process_connect, args=[conn, addr])
        thread.start()
