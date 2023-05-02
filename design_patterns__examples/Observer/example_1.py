#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Observer — Наблюдатель
# SOURCE: https://ru.wikipedia.org/wiki/Наблюдатель_(шаблон_проектирования)
# SOURCE: https://ru.wikipedia.org/wiki/Наблюдатель_(шаблон_проектирования)#Java


from abc import ABC, abstractmethod


# В примере описывается получение данных от метеорологической станции (класс weather_data, рассылатель событий) и
# использование их для вывода на экран (класс CurrentConditionsDisplay, слушатель событий).
# Слушатель регистрируется у наблюдателя с помощью метода register_observer (при этом слушатель заносится в
# список observers). Регистрация происходит в момент создания объекта currentDisplay, т.к. метод register_observer
# применяется в конструкторе.
# При изменении погодных данных вызывается метод notify_observers, который в свою очередь вызывает метод update
# у всех слушателей, передавая им обновлённые данные.


class Observer(ABC):
    @abstractmethod
    def update(self, temperature: float, humidity: float, pressure: int):
        pass


class Observable(ABC):
    @abstractmethod
    def register_observer(self, o: Observer):
        pass

    @abstractmethod
    def remove_observer(self, o: Observer):
        pass

    @abstractmethod
    def notify_observers(self):
        pass


class WeatherData(Observable):
    def __init__(self):
        self.observers = []
        self.temperature: float = None
        self.humidity: float = None
        self.pressure: int = None

    def register_observer(self, o: Observer):
        self.observers.append(o)

    def remove_observer(self, o: Observer):
        self.observers.remove(o)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.temperature, self.humidity, self.pressure)

    def set_measurements(self, temperature: float, humidity: float, pressure: int):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.notify_observers()


class CurrentConditionsDisplay(Observer):
    def __init__(self, weather_data: WeatherData):
        self.weather_data = weather_data
        self.weather_data.register_observer(self)

        self.temperature: float = None
        self.humidity: float = None
        self.pressure: int = None

    def update(self, temperature: float, humidity: float, pressure: int):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure

        self.display()

    def display(self):
        print(
            "Сейчас значения: {:.1f} градусов цельсия и {:.1f}% влажности. Давление {} мм рт. ст.".format(
                self.temperature, self.humidity, self.pressure
            )
        )


if __name__ == "__main__":
    weather_data = WeatherData()
    current_display = CurrentConditionsDisplay(weather_data)

    weather_data.set_measurements(temperature=29, humidity=65, pressure=745)
    weather_data.set_measurements(temperature=39, humidity=70, pressure=760)
    weather_data.set_measurements(temperature=42, humidity=72, pressure=763)
    # Сейчас значения: 29.0 градусов цельсия и 65.0% влажности. Давление 745 мм рт. ст.
    # Сейчас значения: 39.0 градусов цельсия и 70.0% влажности. Давление 760 мм рт. ст.
    # Сейчас значения: 42.0 градусов цельсия и 72.0% влажности. Давление 763 мм рт. ст.
