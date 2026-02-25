#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Flyweight — Приспособленец
# SOURCE: https://ru.wikipedia.org/wiki/Приспособленец_(шаблон_проектирования)


from abc import ABC


# "Flyweight"
class Character(ABC):
    symbol: str
    width: int
    height: int
    ascent: int
    descent: int
    point_size: int

    def display(self, point_size: int) -> None:
        self.point_size = point_size
        print(f"{self.symbol} (point_size {self.point_size})")


# "FlyweightFactory"
class CharacterFactory:
    def __init__(self) -> None:
        self._characters: dict[str, Character] = dict()

    def get_character(self, key: str) -> Character:
        # Uses "lazy initialization"
        character = self._characters.get(key)
        if character is None:
            if key == "A":
                character = CharacterA()

            elif key == "B":
                character = CharacterB()

            # ...

            elif key == "Z":
                character = CharacterZ()

            self._characters[key] = character

        return character


# "ConcreteFlyweight"
class CharacterA(Character):
    def __init__(self) -> None:
        self.symbol = "A"
        self.height = 100
        self.width = 120
        self.ascent = 70
        self.descent = 0


# "ConcreteFlyweight"
class CharacterB(Character):
    def __init__(self) -> None:
        self.symbol = "B"
        self.height = 100
        self.width = 140
        self.ascent = 72
        self.descent = 0


# ... C, D, E, etc.


# "ConcreteFlyweight"
class CharacterZ(Character):
    def __init__(self) -> None:
        self.symbol = "Z"
        self.height = 100
        self.width = 100
        self.ascent = 68
        self.descent = 0


if __name__ == "__main__":
    # Build a document with text
    chars = "AAZZBBZB"

    f = CharacterFactory()

    # Extrinsic state
    point_size = 10

    # For each character use a flyweight object
    for c in chars:
        point_size += 1
        character = f.get_character(c)
        character.display(point_size)
