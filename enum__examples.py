#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# https://docs.python.org/3.5/library/enum.html
from enum import Enum, IntEnum, unique


class Animal(Enum):
    ANT = 1
    BEE = 2
    CAT = 3
    DOG = 4


print(Animal.ANT == Animal.BEE)  # False
print(Animal.ANT == Animal.ANT)  # True
print(Animal.ANT is Animal.ANT)  # True
print(Animal.ANT == 1)  # False
print()

print(Animal)  # <enum 'Animal'>
print(list(Animal))
# [<Animal.ANT: 1>, <Animal.BEE: 2>, <Animal.CAT: 3>, <Animal.DOG: 4>]
print()

for x in Animal:
    print(f'{x}: "{x.name}" = {x.value}')

print()


class Animal2(IntEnum):
    ANT = 1
    BEE = 2
    CAT = 3
    DOG = 4


print(Animal2.ANT == Animal2.BEE)  # False
print(Animal2.ANT == Animal2.ANT)  # True
print(Animal2.ANT is Animal2.ANT)  # True
print(Animal2.ANT == 1)  # True
print()


print()


# https://docs.python.org/3.5/library/enum.html#planet
class Planet(Enum):
    MERCURY = (3.303e23, 2.4397e6)
    VENUS = (4.869e24, 6.0518e6)
    EARTH = (5.976e24, 6.37814e6)
    MARS = (6.421e23, 3.3972e6)
    JUPITER = (1.9e27, 7.1492e7)
    SATURN = (5.688e26, 6.0268e7)
    URANUS = (8.686e25, 2.5559e7)
    NEPTUNE = (1.024e26, 2.4746e7)

    def __init__(self, mass, radius) -> None:
        self.mass = mass  # in kilograms
        self.radius = radius  # in meters

    @property
    def surface_gravity(self):
        # universal gravitational constant  (m3 kg-1 s-2)
        G = 6.67300e-11
        return G * self.mass / (self.radius * self.radius)


print(Planet.EARTH.value)  # (5.976e+24, 6378140.0)
print(Planet.EARTH.surface_gravity)  # 9.802652743337129
print()


class StrEnum(str, Enum):
    pass


@unique
class Color(StrEnum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


print(Color.RED == "red")  # True
print(Color.GREEN == "green")  # True
print(Color.GREEN == "red")  # False
print()
print(Color.RED in Color)  # True
print("red" in Color)  # False
print("red" in Color)  # False
print()
print("Color is " + Color.RED)  # Color is red
print("Color is " + Color.RED + Color.GREEN)  # Color is redgreen
print("Colors: " + ", ".join(Color))  # Colors: red, green, blue
print()

data = [
    {
        "name": "car",
        "color": Color.RED,
    },
    {
        "name": "dog",
        "color": Color.BLUE,
    },
]

print(data)
print(Color("red"))  # Color.red
print(Color("blue"))  # Color.blue
# print(Color('yellow'))  # ValueError: 'yellow' is not a valid Color
print()

import json

print(json.dumps(data, indent=4))
