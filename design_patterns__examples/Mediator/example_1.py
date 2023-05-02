#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Mediator — Посредник
# SOURCE: https://ru.wikipedia.org/wiki/Посредник_(шаблон_проектирования)
# SOURCE: https://refactoring.guru/ru/design-patterns/mediator
# SOURCE: https://refactoring.guru/ru/design-patterns/mediator/csharp/example
# SOURCE: https://refactoring.guru/ru/design-patterns/mediator/python/example


from abc import ABC, abstractmethod


class IMediator(ABC):
    """
    Интерфейс Посредника предоставляет метод, используемый компонентами для
    уведомления посредника о различных событиях. Посредник может реагировать на
    эти события и передавать исполнение другим компонентам.
    """

    @abstractmethod
    def notify(self, sender: object, event: str):
        pass


# Конкретные Посредники реализуют совместное поведение, координируя отдельные компоненты.
class ConcreteMediator(IMediator):
    def __init__(self, component1, component2):
        self._component1 = component1
        self._component1.set_mediator(self)
        self._component2 = component2
        self._component2.set_mediator(self)

    def notify(self, sender: object, event: str):
        print(f'[+] Mediator notify(sender={sender}, event="{event}")')

        if event == "A":
            print("[+] Mediator reacts on A and triggers following operations:")
            self._component2.do_c()

        elif event == "B":
            print("[+] Mediator reacts on B and triggers following operations:")
            print("[-] Nothing!")

        elif event == "D":
            print("[+] Mediator reacts on D and triggers following operations:")
            self._component1.do_b()
            self._component2.do_c()


class BaseComponent(ABC):
    """
    Базовый Компонент обеспечивает базовую функциональность хранения экземпляра
    посредника внутри объектов компонентов.
    """

    def __init__(self, mediator: IMediator = None):
        self._mediator = mediator

    def set_mediator(self, mediator: IMediator):
        self._mediator = mediator


# Конкретные Компоненты реализуют различную функциональность.  Они не зависят от других
# компонентов. Они также не зависят от каких-либо конкретных классов посредников.
class Component1(BaseComponent):
    def do_a(self):
        print("Component 1 does A.")
        self._mediator.notify(self, "A")

    def do_b(self):
        print("Component 1 does B.")
        self._mediator.notify(self, "B")


class Component2(BaseComponent):
    def do_c(self):
        print("Component 2 does C.")
        self._mediator.notify(self, "C")

    def do_d(self):
        print("Component 2 does D.")
        self._mediator.notify(self, "D")


if __name__ == "__main__":
    # Клиентский код
    component1 = Component1()
    component2 = Component2()
    mediator = ConcreteMediator(component1, component2)

    print("Client triggets operation A.")
    component1.do_a()

    print()

    print("Client triggers operation D.")
    component2.do_d()
