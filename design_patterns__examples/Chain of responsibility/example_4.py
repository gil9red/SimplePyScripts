#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Chain of responsibility — Цепочка обязанностей
# SOURCE: https://ru.wikipedia.org/wiki/Цепочка_обязанностей
# SOURCE: https://ru.wikipedia.org/wiki/Цепочка_обязанностей#Пример_на_C++


from abc import ABC, abstractmethod


# Вспомогательный класс, описывающий некоторое преступление
class CriminalAction:
    def __init__(self, complexity: int, description: str):
        # Сложность дела
        self.complexity = complexity

        # Краткое описание преступления
        self.description = description


# Абстрактный полицейский, который может заниматься расследованием преступлений
class Policeman(ABC):
    def __init__(self, deduction: int):
        # Дедукция (умение распутывать сложные дела) у данного полицейского
        self.deduction = deduction

        # Более умелый полицейский, который получит дело, если для текущего оно слишком сложное
        self.next: Policeman = None

    # Расследование
    @abstractmethod
    def _investigate_сoncrete(self, description: str):
        pass

    # Добавляет в цепочку ответственности более опытного полицейского, который сможет принять на себя
    # расследование, если текущий не справится
    def set_next(self, policeman: "Policeman") -> "Policeman":
        self.next = policeman
        return self.next

    # Полицейский начинает расследование или, если дело слишком сложное, передает ее более опытному коллеге
    def investigate(self, criminal_action: CriminalAction):
        if self.deduction < criminal_action.complexity:
            if self.next:
                self.next.investigate(criminal_action)
            else:
                print("Это дело не раскрыть никому.")

        else:
            self._investigate_сoncrete(criminal_action.description)


class MartinRiggs(Policeman):
    def _investigate_сoncrete(self, description: str):
        print('Расследование по делу "' + description + '" ведет сержант Мартин Риггс')


class JohnMcClane(Policeman):
    def _investigate_сoncrete(self, description: str):
        print(
            'Расследование по делу "' + description + '" ведет детектив Джон Макклейн'
        )


class VincentHanna(Policeman):
    def _investigate_сoncrete(self, description: str):
        print(
            'Расследование по делу "' + description + '" ведет лейтенант Винсент Ханна'
        )


if __name__ == "__main__":
    print("OUTPUT:")
    policeman = MartinRiggs(3)  # Полицейский с наименьшим навыком ведения расследований
    # Добавляем ему двух опытных коллег
    policeman.set_next(JohnMcClane(5)).set_next(VincentHanna(8))
    policeman.investigate(
        CriminalAction(2, "Торговля наркотиками из Вьетнама")
    )
    policeman.investigate(
        CriminalAction(7, "Дерзкое ограбление банка в центре Лос-Анджелеса")
    )
    policeman.investigate(
        CriminalAction(5, "Серия взрывов в центре Нью-Йорка")
    )

    # OUTPUT:
    # Расследование по делу "Торговля наркотиками из Вьетнама" ведет сержант Мартин Риггс
    # Расследование по делу "Дерзкое ограбление банка в центре Лос-Анджелеса" ведет лейтенант Винсент Ханна
    # Расследование по делу "Серия взрывов в центре Нью-Йорка" ведет детектив Джон Макклейн
