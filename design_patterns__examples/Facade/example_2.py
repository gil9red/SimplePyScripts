#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Facade — Фасад
# SOURCE: https://ru.wikipedia.org/wiki/Фасад_(шаблон_проектирования)
# SOURCE: https://refactoring.guru/ru/design-patterns/facade
# SOURCE: https://refactoring.guru/ru/design-patterns/facade/python/example


# Реализации отдельных частей компьютера.
# У каждого метода классов имеется какая-то реализация, в данном примере она опущена.


class Subsystem1:
    """
    Подсистема может принимать запросы либо от фасада, либо от клиента
    напрямую. В любом случае, для Подсистемы Фасад – это ещё один клиент, и
    он не является частью Подсистемы.
    """

    def operation_ready(self) -> str:
        return "Subsystem1: Ready!"

    # ...

    def operation_go(self) -> str:
        return "Subsystem1: Go!"


class Subsystem2:
    """
    Некоторые фасады могут работать с разными подсистемами одновременно.
    """

    def operation_ready(self) -> str:
        return "Subsystem2: Get ready!"

    # ...

    def operation_fire(self) -> str:
        return "Subsystem2: Fire!"


class Facade:
    """
    Класс Фасада предоставляет простой интерфейс для сложной логики одной или
    нескольких подсистем. Фасад делегирует запросы клиентов соответствующим
    объектам внутри подсистемы. Фасад также отвечает за управление их
    жизненным циклом. Все это защищает клиента от нежелательной сложности
    подсистемы.
    """

    def __init__(self, subsystem1: Subsystem1, subsystem2: Subsystem2) -> None:
        """
        В зависимости от потребностей вашего приложения вы можете
        предоставить Фасаду существующие объекты подсистемы или заставить
        Фасад создать их самостоятельно.
        """

        self._subsystem1 = subsystem1 or Subsystem1()
        self._subsystem2 = subsystem2 or Subsystem2()

    def operation(self) -> str:
        """
        Методы Фасада удобны для быстрого доступа к сложной функциональности
        подсистем. Однако клиенты получают только часть возможностей
        подсистемы.
        """

        results = [
            "Facade initializes subsystems:",
            self._subsystem1.operation_ready(),
            self._subsystem2.operation_ready(),
            "Facade orders subsystems to perform the action:",
            self._subsystem1.operation_go(),
            self._subsystem2.operation_fire(),
        ]
        return "\n".join(results)


def client_code(facade: Facade) -> None:
    """
    Клиентский код работает со сложными подсистемами через простой интерфейс,
    предоставляемый Фасадом. Когда фасад управляет жизненным циклом
    подсистемы, клиент может даже не знать о существовании подсистемы. Такой
    подход позволяет держать сложность под контролем.
    """

    print(facade.operation())


if __name__ == "__main__":
    # В клиентском коде могут быть уже созданы некоторые объекты подсистемы. В
    # этом случае может оказаться целесообразным инициализировать Фасад с этими
    # объектами вместо того, чтобы позволить Фасаду создавать новые экземпляры.
    subsystem1 = Subsystem1()
    subsystem2 = Subsystem2()
    facade = Facade(subsystem1, subsystem2)
    client_code(facade)
