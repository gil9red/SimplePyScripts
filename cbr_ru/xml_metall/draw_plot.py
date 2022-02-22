#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


from db import MetalRate
from parser import MetalEnum


DATE_FORMAT = '%d/%m/%Y'


# TODO: поддержать и другие металлы
days = []
values = []
for metal_rate in MetalRate.select().where(MetalRate.metal == MetalEnum.Gold):
    days.append(metal_rate.date)
    values.append(metal_rate.amount)


plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(DATE_FORMAT))
plt.gca().xaxis.set_major_locator(mdates.YearLocator(3))

plt.plot(days, values)

title = f"Стоимость грамма золота в рублях за {days[0].strftime(DATE_FORMAT)} - {days[-1].strftime(DATE_FORMAT)}"
plt.xlabel(title)

plt.gcf().autofmt_xdate()

plt.show()
