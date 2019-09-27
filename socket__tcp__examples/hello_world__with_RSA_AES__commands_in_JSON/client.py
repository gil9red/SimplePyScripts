#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from base64 import b64decode, b64encode
import json
import socket

import sys
sys.path.append('..')

from common import send_msg, recv_msg
from utils import CommandEnum
import rsa


def get_command(name: CommandEnum, data: str) -> str:
    return json.dumps({'command': name.name, 'data': data}, ensure_ascii=False)


HOST, PORT = "localhost", 9090


with socket.socket() as sock:
    sock.connect((HOST, PORT))

    key_AES = None

    print(f'Performing RSA key generation!')

    public_key, private_key = rsa.new_keys(key_size=2048)
    print('Key generation completed successfully!')

    public_key_text = public_key.exportKey('PEM').decode('utf-8')
    data = get_command(CommandEnum.NEW_PUBLIC_KEY, public_key_text)

    print(f'Sending ({len(data)}): {data}')
    data = bytes(data, 'utf-8')
    print()

    send_msg(sock, data)

    print('Receiving')

    response_data = recv_msg(sock)
    if response_data:
        print(f'Response ({len(response_data)}): {response_data}')

        rs = json.loads(response_data, encoding='utf-8')

        command = CommandEnum[rs['command']]
        if command == CommandEnum.NEW_PUBLIC_KEY:
            key_AES = rsa.decrypt(b64decode(rs['data']), private_key)
            print('key_AES:', key_AES)

        # TODO: more commands

    print('Close\n')
