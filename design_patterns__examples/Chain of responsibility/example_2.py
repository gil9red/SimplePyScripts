#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Chain of responsibility — Цепочка обязанностей
# SOURCE: https://ru.wikipedia.org/wiki/Цепочка_обязанностей
# SOURCE: https://ru.wikipedia.org/wiki/Цепочка_обязанностей#Пример_на_Python


class Car:
    def __init__(self) -> None:
        self.name = None
        self.km = 11100
        self.fuel = 5
        self.oil = 5


def handle_fuel(car) -> None:
    if car.fuel < 10:
        print("Added fuel")
        car.fuel = 100


def handle_km(car) -> None:
    if car.km > 10000:
        print("Made a car test.")
        car.km = 0


def handle_oil(car) -> None:
    if car.oil < 10:
        print("Added oil")
        car.oil = 100


class Garage:
    def __init__(self) -> None:
        self.handlers = []

    def add_handler(self, handler) -> None:
        self.handlers.append(handler)

    def handle_car(self, car) -> None:
        for handler in self.handlers:
            handler(car)


if __name__ == "__main__":
    handlers = [handle_fuel, handle_km, handle_oil]
    garage = Garage()

    for handle in handlers:
        garage.add_handler(handle)

    garage.handle_car(Car())
