#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as DT
import json
import socket
import threading
import traceback
import random
import uuid

# Для импорта common
import sys
sys.path.append("..")
from common import send_msg, recv_msg
from info_security import InfoSecurity
from utils import CommandEnum, FILE_NAME_PRIVATE_KEY
import rsa


CONNECTION_BY_KEY = dict()

with open(FILE_NAME_PRIVATE_KEY, "rb") as f:
    PRIVATE_KEY = rsa.import_key(f.read())


def process_command(data: bytes, conn, addr) -> bytes:
    rq = json.loads(data, encoding="utf-8")

    command_name = rq["command"]
    command = CommandEnum[command_name]

    if command == CommandEnum.CURRENT_DATETIME:
        rq["data"] = DT.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    elif command == CommandEnum.CURRENT_TIMESTAMP:
        rq["data"] = str(DT.datetime.now().timestamp())

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

                print(f"[*] Sending raw ({len(rs)}): {rs}")
                rs = CONNECTION_BY_KEY[conn].encrypt(rs)

            else:
                key_AES = rsa.decrypt(data, PRIVATE_KEY)
                print("key_AES:", key_AES)

                CONNECTION_BY_KEY[conn] = InfoSecurity(key_AES)
                rs = b""

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
