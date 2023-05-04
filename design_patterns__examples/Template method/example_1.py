#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Template method — Шаблонный метод
# SOURCE: https://ru.wikipedia.org/wiki/Шаблонный_метод_(шаблон_проектирования)


from abc import ABC, abstractmethod


class Unit(ABC):
    """
    Абстрактный отряд. Аттрибуты класса, начинающиеся с подчеркивания в python
    являются protected
    """

    def __init__(self, speed: int) -> None:
        """
        Constructor.

        :param speed: скорость отряда
        """
        self._speed = speed

    def hit_and_run(self) -> None:
        """
        Шаблонный метод
        """
        self._move("вперед")
        self._stop()
        self._attack()
        self._move("назад")

    @abstractmethod
    def _attack(self) -> None:
        pass

    @abstractmethod
    def _stop(self) -> None:
        pass

    def _move(self, direction: str) -> None:
        """
        Передвижение - у всех отрядов одинаковое, в шаблон не входит

        :param direction: направление движения
        """
        self._output("движется {} со скоростью {}".format(direction, self._speed))

    def _output(self, message: str) -> None:
        """
        Вспомогательный метод вывода сообщений, в шаблон не входит

        :param message: выводимое сообщение
        """
        print("Отряд типа {} {}".format(self.__class__.__name__, message))


class Archers(Unit):
    """
    Лучники
    """

    def _attack(self) -> None:
        self._output("обстреливает врага")

    def _stop(self) -> None:
        self._output("останавливается в 100 шагах от врага")


class Cavarlymen(Unit):
    """
    Кавалеристы
    """

    def _attack(self) -> None:
        self._output("на полном скаку врезается во вражеский строй")

    def _stop(self) -> None:
        self._output("летит вперед, не останавливаясь")


if __name__ == "__main__":
    print("OUTPUT:")
    archers = Archers(4)
    archers.hit_and_run()
    cavarlymen = Cavarlymen(8)
    cavarlymen.hit_and_run()

    # OUTPUT:
    # Отряд типа Archers движется вперед со скоростью 4
    # Отряд типа Archers останавливается в 100 шагах от врага
    # Отряд типа Archers обстреливает врага
    # Отряд типа Archers движется назад со скоростью 4
    # Отряд типа Cavarlymen движется вперед со скоростью 8
    # Отряд типа Cavarlymen летит вперед, не останавливаясь
    # Отряд типа Cavarlymen на полном скаку врезается во вражеский строй
    # Отряд типа Cavarlymen движется назад со скоростью 8
