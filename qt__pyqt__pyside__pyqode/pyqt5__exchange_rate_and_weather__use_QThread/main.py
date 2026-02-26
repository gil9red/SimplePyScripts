#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback
import time

from PyQt5 import Qt

from utils import exchange_rate, get_weather


def log_uncaught_exceptions(ex_cls, ex, tb) -> None:
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    Qt.QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class ThreadExchangeRate(Qt.QThread):
    about_exchange_rate = Qt.pyqtSignal(str)

    def __init__(self, parent, currency) -> None:
        super().__init__(parent)

        self.currency = currency

    def run(self) -> None:
        while True:
            print("Start ThreadExchangeRate.currency: " + self.currency)

            value = exchange_rate(self.currency)
            print(f"  ThreadExchangeRate.{self.currency} value: {value}")

            self.about_exchange_rate.emit(value)

            time.sleep(60)


class ThreadGetWeather(Qt.QThread):
    about_weather = Qt.pyqtSignal(str)

    def __init__(self, parent, city) -> None:
        super().__init__(parent)

        self.city = city

    def run(self) -> None:
        while True:
            print("Start ThreadGetWeather.city: " + self.city)

            weather = get_weather(self.city)
            print(f"  ThreadGetWeather.{self.city} weather: {weather}")

            self.about_weather.emit(weather)

            time.sleep(60)


class Window(Qt.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Widget-Info: exchange rate and weather")

        self.exchange_rate_USD = Qt.QLabel()
        self.exchange_rate_EUR = Qt.QLabel()

        self.weather_1 = Qt.QLabel()
        self.weather_2 = Qt.QLabel()
        self.weather_3 = Qt.QLabel()

        layout = Qt.QFormLayout()
        layout.addRow("USD:", self.exchange_rate_USD)
        layout.addRow("EUR:", self.exchange_rate_EUR)

        line = Qt.QFrame()
        line.setFrameShape(Qt.QFrame.HLine)
        line.setFrameShadow(Qt.QFrame.Sunken)
        line.setLineWidth(1)

        layout.addRow(line)

        layout.addRow("Магнитогорск:", self.weather_1)
        layout.addRow("Челябинск:", self.weather_2)
        layout.addRow("Екатеринбург:", self.weather_3)

        self.setLayout(layout)

        self.thread_exchange_rate_USD = ThreadExchangeRate(self, "USD")
        self.thread_exchange_rate_USD.about_exchange_rate.connect(
            self.exchange_rate_USD.setText
        )
        self.thread_exchange_rate_USD.start()

        self.thread_exchange_rate_EUR = ThreadExchangeRate(self, "EUR")
        self.thread_exchange_rate_EUR.about_exchange_rate.connect(
            self.exchange_rate_EUR.setText
        )
        self.thread_exchange_rate_EUR.start()

        self.thread_weather_1 = ThreadGetWeather(self, "Магнитогорск")
        self.thread_weather_1.about_weather.connect(self.weather_1.setText)
        self.thread_weather_1.start()

        self.thread_weather_2 = ThreadGetWeather(self, "Челябинск")
        self.thread_weather_2.about_weather.connect(self.weather_2.setText)
        self.thread_weather_2.start()

        self.thread_weather_3 = ThreadGetWeather(self, "Екатеринбург")
        self.thread_weather_3.about_weather.connect(self.weather_3.setText)
        self.thread_weather_3.start()


if __name__ == "__main__":
    app = Qt.QApplication([])

    mw = Window()
    mw.show()

    app.exec()
