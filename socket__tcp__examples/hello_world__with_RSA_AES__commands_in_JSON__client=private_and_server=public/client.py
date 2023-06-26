#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import socket
import sys

from base64 import b64decode

sys.path.append("..")
from common import send_msg, recv_msg
from info_security import InfoSecurity
from utils import CommandEnum
import rsa


def get_command(name: CommandEnum, data: str = None) -> str:
    return json.dumps({"command": name.name, "data": data}, ensure_ascii=False)


def send_command(name: CommandEnum, data: str = None) -> dict | None:
    data = get_command(name, data)

    data = bytes(data, "utf-8")

    # Публичный ключ передается в не зашифрованном виде
    if name != CommandEnum.SEND_PUBLIC_KEY:
        print(f"[*] Sending raw ({len(data)}): {data}")
        data = DATA["info_security"].encrypt(data)

    print(f"[+] Sending ({len(data)}): {data}")
    send_msg(sock, data)

    print("[+] Receiving...")
    response_data = recv_msg(sock)
    if not response_data:
        return

    print(f"[+] Response ({len(response_data)}): {response_data}")

    # AES ключ, зашифрованный публичным ключом, передается в не зашифрованном виде
    if name != CommandEnum.SEND_PUBLIC_KEY:
        response_data = DATA["info_security"].decrypt(response_data)
        print(f"[*] Response raw ({len(response_data)}): {response_data}")

    rs = json.loads(response_data, encoding="utf-8")

    command = CommandEnum[rs["command"]]
    if command != name:
        raise Exception(f"Received response to another command. ")

    return rs


HOST, PORT = "localhost", 9090
DATA = {"info_security": None}


with socket.socket() as sock:
    sock.connect((HOST, PORT))

    print(f"[+] Performing RSA key generation!")

    public_key, private_key = rsa.new_keys(key_size=2048)
    print("[+] Key generation completed successfully!")

    public_key_text = public_key.exportKey("PEM").decode("utf-8")
    rs = send_command(CommandEnum.SEND_PUBLIC_KEY, public_key_text)
    if rs:
        print(rs)

        key = rsa.decrypt(b64decode(rs["data"]), private_key)
        print("[+] key_AES:", key)

        DATA["info_security"] = InfoSecurity(key)

    else:
        print("[-] Need AES key from server!")
        sys.exit()

    print("\n")

    for command in [
        CommandEnum.CURRENT_DATETIME,
        CommandEnum.CURRENT_TIMESTAMP,
        CommandEnum.RANDOM,
        CommandEnum.RANDOM,
        CommandEnum.GUID,
        CommandEnum.GUID,
    ]:
        rs = send_command(command)
        if rs:
            print(rs)
            print(f"{command.name}: {rs['data']}")
        else:
            print("[-] No answer!")

        print()

    print("[+] Close\n")
