#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Chain of responsibility — Цепочка обязанностей
# SOURCE: https://ru.wikipedia.org/wiki/Цепочка_обязанностей
# SOURCE: https://refactoring.guru/ru/design-patterns/chain-of-responsibility/python/example


from abc import ABC, abstractmethod
from typing import Any, Optional


class Handler(ABC):
    """
    Интерфейс Обработчика объявляет метод построения цепочки обработчиков. Он
    также объявляет метод для выполнения запроса.
    """

    @abstractmethod
    def set_next(self, handler: "Handler") -> "Handler":
        pass

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        pass


class AbstractHandler(Handler):
    """
    Поведение цепочки по умолчанию может быть реализовано внутри базового класса
    обработчика.
    """

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        # Возврат обработчика отсюда позволит связать обработчики простым
        # способом, вот так:
        # monkey.set_next(squirrel).set_next(dog)
        return handler

    @abstractmethod
    def handle(self, request: Any) -> Optional[str]:
        if self._next_handler:
            return self._next_handler.handle(request)

        return None


"""
Все Конкретные Обработчики либо обрабатывают запрос, либо передают его
следующему обработчику в цепочке.
"""


class MonkeyHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request == "Banana":
            return f"Monkey: I'll eat the {request}"
        else:
            return super().handle(request)


class SquirrelHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request == "Nut":
            return f"Squirrel: I'll eat the {request}"
        else:
            return super().handle(request)


class DogHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request == "MeatBall":
            return f"Dog: I'll eat the {request}"
        else:
            return super().handle(request)


def client_code(handler: Handler) -> None:
    """
    Обычно клиентский код приспособлен для работы с единственным обработчиком. В
    большинстве случаев клиенту даже неизвестно, что этот обработчик является
    частью цепочки.
    """

    for food in ["Nut", "Banana", "Cup of coffee"]:
        print(f"\nClient: Who wants a {food}?")
        result = handler.handle(food)
        if result:
            print(f"  {result}", end="")
        else:
            print(f"  {food} was left untouched.", end="")

    print()


def print_chain(handler: Handler) -> None:
    chain = []

    while handler:
        name = handler.__class__.__name__.replace("Handler", "")
        chain.append(name)
        handler = handler._next_handler

    print("Chain: " + " > ".join(chain))


if __name__ == "__main__":
    monkey = MonkeyHandler()
    squirrel = SquirrelHandler()
    dog = DogHandler()

    monkey.set_next(squirrel).set_next(dog)

    # Example print chain
    #
    # Chain: MonkeyHandler -> SquirrelHandler -> DogHandler
    print_chain(monkey)
    # Chain: Squirrel > Dog
    print_chain(squirrel)
    print()

    # Клиент должен иметь возможность отправлять запрос любому обработчику, а не
    # только первому в цепочке.
    print("OUTPUT:")

    print("Chain: Monkey > Squirrel > Dog")
    client_code(monkey)

    print(f'\n{"-"*30}\n')

    print("Subchain: Squirrel > Dog")
    client_code(squirrel)

    # OUTPUT:
    # Chain: Monkey > Squirrel > Dog
    #
    # Client: Who wants a Nut?
    #   Squirrel: I'll eat the Nut
    # Client: Who wants a Banana?
    #   Monkey: I'll eat the Banana
    # Client: Who wants a Cup of coffee?
    #   Cup of coffee was left untouched.
    #
    # ------------------------------
    #
    # Subchain: Squirrel > Dog
    #
    # Client: Who wants a Nut?
    #   Squirrel: I'll eat the Nut
    # Client: Who wants a Banana?
    #   Banana was left untouched.
    # Client: Who wants a Cup of coffee?
    #   Cup of coffee was left untouched.
