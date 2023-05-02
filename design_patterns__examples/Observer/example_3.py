#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Observer — Наблюдатель
# SOURCE: https://ru.wikipedia.org/wiki/Наблюдатель_(шаблон_проектирования)
# SOURCE: https://refactoring.guru/ru/design-patterns/observer/python/example


from abc import ABC, abstractmethod
from random import randrange


class Observer(ABC):
    """
    Интерфейс Наблюдателя объявляет метод уведомления, который издатели
    используют для оповещения своих подписчиков.
    """

    @abstractmethod
    def update(self, subject: "Subject") -> None:
        """
        Получить обновление от субъекта.
        """
        pass


class Subject(ABC):
    """
    Интферфейс издателя объявляет набор методов для управлениями подпискичами.
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """
        Присоединяет наблюдателя к издателю.
        """
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """
        Отсоединяет наблюдателя от издателя.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Уведомляет всех наблюдателей о событии.
        """
        pass


class ConcreteSubject(Subject):
    """
    Издатель владеет некоторым важным состоянием и оповещает наблюдателей о его
    изменениях.
    """

    state: int = None
    """
    Для удобства в этой переменной хранится состояние Издателя, необходимое всем
    подписчикам.
    """

    _observers: list[Observer] = []
    """
    Список подписчиков. В реальной жизни список подписчиков может храниться в
    более подробном виде (классифицируется по типу события и т.д.)
    """

    def attach(self, observer: Observer) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    """
    Методы управления подпиской.
    """

    def notify(self) -> None:
        """
        Запуск обновления в каждом подписчике.
        """

        print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def some_business_logic(self) -> None:
        """
        Обычно логика подписки – только часть того, что делает Издатель.
        Издатели часто содержат некоторую важную бизнес-логику, которая
        запускает метод уведомления всякий раз, когда должно произойти что-то
        важное (или после этого).
        """

        print("\nSubject: I'm doing something important.")
        self.state = randrange(0, 10)

        print(f"Subject: My state has just changed to: {self.state}")
        self.notify()


"""
Конкретные Наблюдатели реагируют на обновления, выпущенные Издателем, к которому
они прикреплены.
"""


class ConcreteObserverA(Observer):
    def update(self, subject: Subject) -> None:
        if subject.state < 3:
            print("ConcreteObserverA: Reacted to the event")


class ConcreteObserverB(Observer):
    def update(self, subject: Subject) -> None:
        if subject.state == 0 or subject.state >= 2:
            print("ConcreteObserverB: Reacted to the event")


if __name__ == "__main__":
    # Клиентский код.
    subject = ConcreteSubject()

    observer_a = ConcreteObserverA()
    subject.attach(observer_a)

    observer_b = ConcreteObserverB()
    subject.attach(observer_b)

    subject.some_business_logic()
    subject.some_business_logic()

    subject.detach(observer_a)

    subject.some_business_logic()

    # Subject: Attached an observer.
    # Subject: Attached an observer.
    #
    # Subject: I'm doing something important.
    # Subject: My state has just changed to: 0
    # Subject: Notifying observers...
    # ConcreteObserverA: Reacted to the event
    # ConcreteObserverB: Reacted to the event
    #
    # Subject: I'm doing something important.
    # Subject: My state has just changed to: 5
    # Subject: Notifying observers...
    # ConcreteObserverB: Reacted to the event
    #
    # Subject: I'm doing something important.
    # Subject: My state has just changed to: 0
    # Subject: Notifying observers...
    # ConcreteObserverB: Reacted to the event
