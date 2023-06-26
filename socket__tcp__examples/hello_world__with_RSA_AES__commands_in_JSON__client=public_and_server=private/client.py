#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import secrets
import socket

import sys
sys.path.append("..")
from common import send_msg, recv_msg
from info_security import InfoSecurity
from utils import CommandEnum, FILE_NAME_PUBLIC_KEY
import rsa


with open(FILE_NAME_PUBLIC_KEY, "rb") as f:
    PUBLIC_KEY = rsa.import_key(f.read())


def get_command(name: CommandEnum, data: str = None) -> str:
    return json.dumps({"command": name.name, "data": data}, ensure_ascii=False)


def send_command(data: bytes = None, key: InfoSecurity = None) -> dict | None:
    print(f"[+] Sending raw ({len(data)}): {data}")

    if key:
        data = key.encrypt(data)
        print(f"[+] Sending ({len(data)}): {data}")

    send_msg(sock, data)

    print("[+] Receiving...")

    response_data = recv_msg(sock)
    if not response_data:
        return

    print(f"[+] Response ({len(response_data)}): {response_data}")

    if key:
        response_data = key.decrypt(response_data)
        print(f"[*] Response raw ({len(response_data)}): {response_data}")

    rs = json.loads(response_data, encoding="utf-8")
    return rs


HOST, PORT = "localhost", 9090


with socket.socket() as sock:
    sock.connect((HOST, PORT))

    print(f"[+] Performing session AES key generation!")

    # Придумываем ключ для шифрования сообщений
    key_AES = secrets.token_bytes(32)
    print("key_AES:", key_AES)

    key = InfoSecurity(key_AES)
    print("[+] Key generation completed successfully!")

    encrypted_data = rsa.encrypt(key_AES, PUBLIC_KEY)

    rs = send_command(encrypted_data, key=None)
    if rs:
        print(rs)

    print("\n")

    for command in [
        CommandEnum.CURRENT_DATETIME,
        CommandEnum.CURRENT_TIMESTAMP,
        CommandEnum.RANDOM,
        CommandEnum.RANDOM,
        CommandEnum.GUID,
        CommandEnum.GUID,
    ]:
        data = get_command(command)
        data = bytes(data, "utf-8")

        rs = send_command(data, key)
        if rs:
            print(rs)
            print(f"{command.name}: {rs['data']}")
        else:
            print("[-] No answer!")

        print()

    print("[+] Close\n")
