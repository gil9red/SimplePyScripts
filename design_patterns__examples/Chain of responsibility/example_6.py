#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Chain of responsibility — Цепочка обязанностей
# SOURCE: https://ru.wikipedia.org/wiki/Цепочка_обязанностей
# SOURCE: https://refactoring.guru/ru/design-patterns/chain-of-responsibility/java/example


from abc import ABC, abstractmethod
from typing import Dict
import time


def get_timestamp() -> int:
    return int(time.time())


# Базовый класс цепочки.
class Middleware(ABC):
    def __init__(self):
        self._next: "Middleware" = None

    # Помогает строить цепь из объектов-проверок.
    def link_with(self, next: "Middleware") -> "Middleware":
        self._next = next
        return next

    # Подклассы реализуют в этом методе конкретные проверки.
    @abstractmethod
    def check(self, email: str, password: str) -> bool:
        pass

    # Запускает проверку в следующем объекте или завершает проверку, если мы в
    # последнем элементе цепи.
    def _check_next(self, email: str, password: str) -> bool:
        if not self._next:
            return True

        return self._next.check(email, password)


# Конкретный элемент цепи обрабатывает запрос по-своему.
class ThrottlingMiddleware(Middleware):
    def __init__(self, request_per_minute: int):
        super().__init__()

        self._request: int = 0
        self._request_per_minute: int = request_per_minute
        self._current_time: int = get_timestamp()

    # Обратите внимание, вызов _check_next() можно вставить как в начале этого
    # метода, так и в середине или в конце.
    # Это даёт еще один уровень гибкости по сравнению с проверками в цикле.
    # Например, элемент цепи может пропустить все остальные проверки вперёд и
    # запустить свою проверку в конце.
    def check(self, email: str, password: str) -> bool:
        if get_timestamp() > self._current_time + 60:
            self._request = 0
            self._current_time = get_timestamp()

        self._request += 1

        if self._request > self._request_per_minute:
            print("Request limit exceeded!")
            return False

        return self._check_next(email, password)


# Конкретный элемент цепи обрабатывает запрос по-своему.
class UserExistsMiddleware(Middleware):
    def __init__(self, server: "Server"):
        super().__init__()

        self._server: Server = server

    def check(self, email: str, password: str) -> bool:
        if not self._server.has_email(email):
            print("This email is not registered!")
            return False

        if not self._server.is_valid_password(email, password):
            print("Wrong password!")
            return False

        return self._check_next(email, password)


# Конкретный элемент цепи обрабатывает запрос по-своему.
class RoleCheckMiddleware(Middleware):
    def check(self, email: str, password: str) -> bool:
        if email == "admin@example.com":
            print("Hello, admin!")
            return True

        print("Hello, user!")
        return self._check_next(email, password)


# Класс сервера.
class Server:
    def __init__(self):
        self._users: Dict[str, str] = dict()
        self._middleware: Middleware = None

    # Клиент подаёт готовую цепочку в сервер. Это увеличивает гибкость и
    # упрощает тестирование класса сервера.
    def set_middleware(self, middleware: Middleware):
        self._middleware = middleware

    # Сервер получает email и пароль от клиента и запускает проверку
    # авторизации у цепочки.
    def log_in(self, email: str, password: str) -> bool:
        if self._middleware.check(email, password):
            print("Authorization have been successful!")

            # Здесь должен быть какой-то полезный код, работающий для
            # авторизированных пользователей.
            return True

        return False

    def register(self, email: str, password: str):
        self._users[email] = password

    def has_email(self, email: str) -> bool:
        return email in self._users

    def is_valid_password(self, email: str, password: str) -> bool:
        return self._users.get(email) == password


if __name__ == "__main__":
    server = Server()
    server.register("admin@example.com", "admin_pass")
    server.register("user@example.com", "user_pass")
    server.register("foo@example.com", "bar")

    # Проверки связаны в одну цепь. Клиент может строить различные цепи,
    # используя одни и те же компоненты.
    middleware = ThrottlingMiddleware(request_per_minute=2)
    middleware.link_with(UserExistsMiddleware(server)).link_with(RoleCheckMiddleware())

    # Сервер получает цепочку от клиентского кода.
    server.set_middleware(middleware)

    print("OUTPUT:")

    while True:
        email = input("Enter email: ")
        password = input("Input password: ")
        success = server.log_in(email, password)
        if not success:
            # ignore
            pass

        print()

    # OUTPUT:
    # Enter email: admin@example.com
    # Input password: admin_pass
    # Hello, admin!
    # Authorization have been successful!
    #
    # Enter email: user@example.com
    # Input password: user_pass
    # Hello, user!
    # Authorization have been successful!
