#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as dt
import json
import secrets
import socket
import threading
import traceback
import random
import uuid

from base64 import b64encode

# Для импорта common
import sys
sys.path.append("..")
from common import send_msg, recv_msg
from info_security import InfoSecurity
from utils import CommandEnum
import rsa


CONNECTION_BY_KEY = dict()


def process_command(data: bytes, conn, addr) -> bytes:
    rq = json.loads(data, encoding="utf-8")

    command_name = rq["command"]
    command = CommandEnum[command_name]

    if command == CommandEnum.SEND_PUBLIC_KEY:
        # Публичный ключ от клиента
        public_key = rsa.import_key(rq["data"])

        # Придумываем ключ для шифрования сообщений
        key_AES = secrets.token_bytes(32)
        print("key_AES:", key_AES)
        CONNECTION_BY_KEY[conn] = InfoSecurity(key_AES)

        # Шифруем ключ для сообщений публичным ключом клиента
        encrypted = b64encode(rsa.encrypt(key_AES, public_key)).decode("utf-8")
        rq["data"] = encrypted

    elif command == CommandEnum.CURRENT_DATETIME:
        rq["data"] = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    elif command == CommandEnum.CURRENT_TIMESTAMP:
        rq["data"] = str(dt.datetime.now().timestamp())

    elif command == CommandEnum.RANDOM:
        rq["data"] = str(random.randint(0, 1000000))

    elif command == CommandEnum.GUID:
        rq["data"] = str(uuid.uuid4())

    else:
        rq["data"] = f'<Unsupported command="{command}">'

    return json.dumps(rq, ensure_ascii=False).encode("utf-8")


def process_connect(conn, addr):
    print(f"[+] New connection from {addr}")

    try:
        while True:
            data = recv_msg(conn)
            if not data:
                break

            print(f"[+] Receiving ({len(data)}): {data}")

            # Проверка, что этот запрос уже не первый, т.к. то, что AES уже есть
            # и что, нужно расшифровавывать запрос
            is_existing_connect = conn in CONNECTION_BY_KEY
            if is_existing_connect:
                data = CONNECTION_BY_KEY[conn].decrypt(data)
                print(f"[*] Receiving raw ({len(data)}): {data}")

            rs = process_command(data, conn, addr)

            if is_existing_connect:
                print(f"[*] Sending raw ({len(rs)}): {rs}")
                rs = CONNECTION_BY_KEY[conn].encrypt(rs)

            print(f"[+] Sending ({len(rs)}): {rs}")
            send_msg(conn, rs)

            print()

    except:
        print(traceback.format_exc())

    finally:
        conn.close()

        if conn in CONNECTION_BY_KEY:
            CONNECTION_BY_KEY.pop(conn)

        print(f"[+] Closed connection from {addr}")
        print()


HOST, PORT = "", 9090


with socket.socket() as sock:
    print("[+] Server created")

    sock.bind((HOST, PORT))
    print("[+] Server bind complete")

    sock.listen()
    print(f"[+] Server now listening: {sock.getsockname()}")
    print()

    while True:
        conn, addr = sock.accept()

        thread = threading.Thread(target=process_connect, args=[conn, addr])
        thread.start()
