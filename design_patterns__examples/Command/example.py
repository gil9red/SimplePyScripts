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
    def start_engine(self):
        print("Запустить двигатель")
    
    def stop_engine(self):
        print("Остановить двигатель")
    

class StartCar(Command):
    def __init__(self, car: Car):
        self.car: Car = car
    
    def execute(self):
        self.car.start_engine()
    

class StopCar(Command):
    def __init__(self, car: Car):
        self.car: Car = car
    
    def execute(self):
        self.car.stop_engine()
    

class CarInvoker:
    def __init__(self, command: Command):
        self.command: Command = command
    
    def execute(self):
        self.command.execute()


if __name__ == "__main__":
    car = Car()

    startCar = StartCar(car)
    stopCar = StopCar(car)

    carInvoker = CarInvoker(startCar)
    carInvoker.execute()

    stopCar.execute()
