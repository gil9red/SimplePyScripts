#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install pyowm
import pyowm


API_KEY = "87c7712a9b72646a269102230858837b"
place = "Магнитогорск"

owm = pyowm.OWM(API_KEY)
observation = owm.weather_at_place(place)
w = observation.get_weather()
temperature = w.get_temperature("celsius")["temp"]
status = w.get_status()

print("Температура: {} °C".format(temperature))
print("Небо: {}".format(status))
