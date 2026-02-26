#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: http://andreymal.org/socket3/


import socket
import time

from threading import Thread


def send_answer(conn, status="200 OK", typ="text/plain; charset=utf-8", data="") -> None:
    data = data.encode("utf-8")

    conn.send(b"GET HTTP/1.1 " + status.encode("utf-8") + b"\r\n")
    conn.send(b"Server: simplehttp\r\n")
    conn.send(b"Connection: close\r\n")
    conn.send(b"Content-Type: " + typ.encode("utf-8") + b"\r\n")
    conn.send(b"Content-Length: " + str(len(data)).encode() + b"\r\n")
    conn.send(b"\r\n")  # После пустой строки в HTTP начинаются данные
    conn.send(data)


def parse(conn) -> None:  # Обработка соединения в отдельной функции
    try:
        data = b""

        while b"\r\n" not in data:  # Ждём первую строку
            tmp = conn.recv(1024)

            # Сокет закрыли, пустой объект
            if not tmp:
                break
            else:
                data += tmp

        # Данные не пришли
        if not data:
            return

        udata = data.decode("utf-8")

        # берём только первую строку
        udata = udata.split("\r\n", 1)[0]

        # разбиваем по пробелам нашу строку
        method, address, protocol = udata.split(" ", 2)

        # if method != "GET" or address != "/time.html":
        #     send_answer(conn, "404 Not Found", data="Не найдено")
        #     return

        answer = """<!DOCTYPE html>"""
        answer += """<html><head><title>Время</title></head><body><h1>"""
        answer += time.strftime("%H:%M:%S %d.%m.%Y")
        answer += """</h1></body></html>"""

        send_answer(conn, typ="text/html; charset=utf-8", data=answer)

    except:
        send_answer(conn, "500 Internal Server Error", data="Ошибка")

    finally:
        conn.close()


HOST = "localhost"
PORT = 9090


if __name__ == "__main__":
    sock = socket.socket()
    print("Socket created")

    sock.bind((HOST, PORT))
    print("Socket bind complete")

    sock.listen()
    print("Socket now listening: http://{}:{}".format(*sock.getsockname()))
    print()

    try:
        # Работаем постоянно
        while True:
            conn, addr = sock.accept()
            print("New connection from " + addr[0])

            thread = Thread(target=parse, args=[conn])
            thread.start()

    finally:
        sock.close()
