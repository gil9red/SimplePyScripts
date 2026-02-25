#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.wikipedia.org/wiki/Фабричный_метод_(шаблон_проектирования)


from abc import ABC, abstractmethod


class Animal(ABC):
    @staticmethod
    def initial(animal: str) -> "Animal":
        if animal == "Lion":
            return Lion()
        elif animal == "Cat":
            return Cat()

        raise Exception(f'Unsupported animal "{animal}"')

    @abstractmethod
    def voice(self) -> None:
        pass


class Lion(Animal):
    def voice(self) -> None:
        print("Rrrrrrrr i'm the lion")


class Cat(Animal):
    def voice(self) -> None:
        print("Meow, meow i'm the kitty")


if __name__ == "__main__":
    animal_1 = Animal.initial("Lion")
    animal_2 = Animal.initial("Cat")

    animal_1.voice()
    animal_2.voice()
