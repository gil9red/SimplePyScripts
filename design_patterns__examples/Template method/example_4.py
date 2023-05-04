#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Template def — Шаблонный метод
# SOURCE: https://ru.wikipedia.org/wiki/Шаблонный_метод_(шаблон_проектирования)
# SOURCE: https://refactoring.guru/ru/design-patterns/template-method


from abc import ABC, abstractmethod
from typing import Optional


class Map:
    def center(self) -> ...:
        pass


class GameAI(ABC):
    def __init__(self):
        self.scouts = []
        self.warriors = []
        self.map = Map()

    # Шаблонный метод должен быть задан в базовом классе. Он
    # состоит из вызовов методов в определённом порядке. Чаще
    # всего эти методы являются шагами некоего алгоритма.
    def turn(self):
        self.collect_resources()
        self.build_structures()
        self.build_units()
        self.attack()

    # Некоторые из этих методов могут быть реализованы прямо в базовом классе.
    def collect_resources(self):
        for s in self.build_structures():
            s.collect()

    # А некоторые могут быть полностью абстрактными.
    @abstractmethod
    def build_structures(self) -> list["Structure"]:
        pass

    @abstractmethod
    def build_units(self):
        pass

    # Кстати, шаблонных методов в классе может быть несколько.
    def attack(self):
        enemy = self.closest_enemy()

        if enemy is None:
            self.send_scouts(self.map.center)
        else:
            self.send_warriors(enemy.position)

    def closest_enemy(self) -> Optional["Enemy"]:
        ...

    @abstractmethod
    def send_scouts(self, position):
        pass

    @abstractmethod
    def send_warriors(self, position):
        pass


# Подклассы могут предоставлять свою реализацию шагов
# алгоритма, не изменяя сам шаблонный метод.
class OrcsAI(GameAI):
    def build_structures(self) -> list["Structure"]:
        structures = []

        there_are_some_resources: bool = ...

        if there_are_some_resources:
            # Строить фермы, затем бараки, а потом цитадель.
            ...

        return structures

    def build_units(self):
        there_are_plenty_of_resources: bool = ...
        there_are_no_scouts: bool = ...

        if there_are_plenty_of_resources:
            if there_are_no_scouts:
                # Построить раба и добавить в группу разведчиков.
                ...
            else:
                # Построить пехотинца и добавить в группу воинов.
                ...

    # ...

    def send_scouts(self, position):
        if self.scouts:
            # Отправить разведчиков на позицию.
            ...

    def send_warriors(self, position):
        if len(self.warriors) > 5:
            # Отправить воинов на позицию.
            ...


# Подклассы могут не только реализовывать абстрактные шаги, но
# и переопределять шаги, уже реализованные в базовом классе.
class MonstersAI(GameAI):
    def collect_resources(self):
        # Ничего не делать.
        pass

    def build_structures(self):
        # Ничего не делать.
        pass

    def build_units(self):
        # Ничего не делать.
        pass

    def send_scouts(self, position):
        if self.scouts:
            # Отправить разведчиков на позицию.
            ...

    def send_warriors(self, position):
        if len(self.warriors) > 5:
            # Отправить воинов на позицию.
            ...


if __name__ == "__main__":
    ai = MonstersAI()
    ai.turn()

    ai = OrcsAI()
    ai.turn()
