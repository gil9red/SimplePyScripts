#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Mediator — Посредник
# SOURCE: https://ru.wikipedia.org/wiki/Посредник_(шаблон_проектирования)
# SOURCE: https://javarush.ru/groups/posts/584-patternih-proektirovanija


class Mediator:
    @staticmethod
    def send_message(user: "User", msg: str):
        print(f"{user.name}: {msg}")


class User:
    def __init__(self, name: str):
        self.name = name

    def send_message(self, msg: str):
        Mediator.send_message(self, msg)


if __name__ == "__main__":
    user1 = User("user1")
    user2 = User("user2")
    user1.send_message("message1")
    user2.send_message("message2")

    # user1: message1
    # user2: message2
