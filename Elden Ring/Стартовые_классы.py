#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
from dataclasses import dataclass

from bs4 import Tag

from common import parse


@dataclass
class Class:
    clss: str
    level: int
    health: int
    vigor: int
    endurance: int
    dexterity: int
    faith: int
    intelligence: int
    strength: int
    mind: int
    arcane: int

    @classmethod
    def parse_from(cls, tr: Tag) -> 'Class':
        cells = [
            el.get_text(strip=True)
            for el in tr.find_all(name=re.compile('th|td'), recursive=False)
        ]
        clss = cells[0]               # Класс
        level = int(cells[1])         # Уровень
        health = int(cells[2])        # Здоровье
        vigor = int(cells[3])         # Жизненная сила
        endurance = int(cells[4])     # Стойкость
        dexterity = int(cells[5])     # Ловкость
        faith = int(cells[6])         # Вера
        intelligence = int(cells[7])  # Мудрость
        strength = int(cells[8])      # Сила
        mind = int(cells[9])          # Интеллект
        arcane = int(cells[10])       # Колдовство

        return cls(
            clss=clss,
            level=level,
            health=health,
            vigor=vigor,
            endurance=endurance,
            dexterity=dexterity,
            faith=faith,
            intelligence=intelligence,
            strength=strength,
            mind=mind,
            arcane=arcane,
        )

    def get_total_stats(self, for_level: int = 0) -> int:
        total = (
                self.vigor + self.endurance + self.dexterity + self.faith
                + self.intelligence + self.strength + self.mind + self.arcane
        )
        # Добавляем очки характеристик от разницы уровней
        if for_level > self.level:
            total += for_level - self.level

        return total


URL = 'https://eldenring.fandom.com/ru/wiki/Стартовые_классы'


def get_classes() -> list[Class]:
    _, root = parse(URL)

    return [
        Class.parse_from(tr)
        for tr in root.select_one('table').select('tr')[1:]
    ]


if __name__ == '__main__':
    classes = get_classes()
    for obj in classes:
        print(obj)
    """
    Class(clss='Бродяга', level=9, health=522, vigor=15, endurance=11, dexterity=13, faith=9, intelligence=9, strength=14, mind=10, arcane=7)
    Class(clss='Воин', level=8, health=434, vigor=11, endurance=11, dexterity=16, faith=8, intelligence=10, strength=10, mind=12, arcane=9)
    Class(clss='Герой', level=7, health=499, vigor=14, endurance=12, dexterity=9, faith=8, intelligence=7, strength=16, mind=9, arcane=11)
    Class(clss='Бандит', level=5, health=414, vigor=10, endurance=10, dexterity=13, faith=8, intelligence=9, strength=9, mind=11, arcane=14)
    Class(clss='Астролог', level=6, health=396, vigor=9, endurance=9, dexterity=12, faith=7, intelligence=16, strength=8, mind=15, arcane=9)
    Class(clss='Пророк', level=7, health=414, vigor=10, endurance=8, dexterity=10, faith=16, intelligence=7, strength=11, mind=14, arcane=10)
    Class(clss='Самурай', level=9, health=455, vigor=12, endurance=13, dexterity=15, faith=8, intelligence=9, strength=12, mind=11, arcane=8)
    Class(clss='Заключённый', level=9, health=434, vigor=11, endurance=11, dexterity=14, faith=6, intelligence=14, strength=11, mind=12, arcane=9)
    Class(clss='Духовник', level=10, health=414, vigor=10, endurance=10, dexterity=12, faith=14, intelligence=9, strength=12, mind=13, arcane=9)
    Class(clss='Мерзавец', level=1, health=414, vigor=10, endurance=10, dexterity=10, faith=10, intelligence=10, strength=10, mind=10, arcane=10)
    """
