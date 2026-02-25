#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Command — Команда
# SOURCE: https://ru.wikipedia.org/wiki/Команда_(шаблон_проектирования)
# SOURCE: https://javarush.ru/groups/posts/584-patternih-proektirovanija


from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class Car:
    def start_engine(self) -> None:
        print("Запустить двигатель")

    def stop_engine(self) -> None:
        print("Остановить двигатель")


class StartCar(Command):
    def __init__(self, car: Car) -> None:
        self.car: Car = car

    def execute(self) -> None:
        self.car.start_engine()


class StopCar(Command):
    def __init__(self, car: Car) -> None:
        self.car: Car = car

    def execute(self) -> None:
        self.car.stop_engine()


class CarInvoker:
    def __init__(self, command: Command) -> None:
        self.command: Command = command

    def execute(self) -> None:
        self.command.execute()


if __name__ == "__main__":
    car = Car()

    startCar = StartCar(car)
    stopCar = StopCar(car)

    carInvoker = CarInvoker(startCar)
    carInvoker.execute()

    stopCar.execute()
