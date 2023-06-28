#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from tkinter import *

# pip install pyowm
import pyowm


API_KEY = "87c7712a9b72646a269102230858837b"


def get_weather_info(api_key, place):
    owm = pyowm.OWM(api_key)
    observation = owm.weather_at_place(place)
    w = observation.get_weather()
    temperature = w.get_temperature("celsius")["temp"]
    status = w.get_status()

    return temperature, status


root = Tk()
root.title("Погода")
root.geometry("150x100")

label = Label()
label2 = Label()

label.grid()
label2.grid()


def update_clock():
    temperature, status = get_weather_info(api_key=API_KEY, place="Donetsk")
    print(temperature, status)

    label.configure(text="Температура: " + str(temperature))
    label2.configure(text="Небо: " + str(status))

    # Вызов каждую секунду
    root.after(1000, update_clock)


# Сразу вызываем, чтобы виджеты заполнились
update_clock()

root.mainloop()
