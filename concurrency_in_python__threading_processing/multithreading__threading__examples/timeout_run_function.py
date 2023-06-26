#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
from threading import Thread, current_thread


class User:
    def __init__(self, name):
        self.name = name

    def post_msg(self):
        time.sleep(3)

        # Написать пользователю
        print(f"Hi, {self.name}! current_thread: {current_thread()}")


user_1 = User("Vasya")
user_1.post_msg()

user_2 = User("Petya")
Thread(target=user_2.post_msg).start()


def foo(name):
    time.sleep(5)

    # Написать пользователю
    print(f"Hi, {name}! current_thread: {current_thread()}")


Thread(target=lambda: foo("Thread")).start()
