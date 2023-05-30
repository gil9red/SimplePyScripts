#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from collections import deque
from datetime import datetime as dt

import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.dates import date2num

import psutil


N = 600
x = deque([date2num(dt.now())], maxlen=N)
y = deque([0], maxlen=N)

fig, ax = plt.subplots(figsize=(8, 3))
(line,) = ax.plot_date(x, y, marker="")

ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)


def get_data():
    return psutil.cpu_percent(0.15)


def animate(i):
    x.append(date2num(dt.now()))
    y.append(get_data())
    ax.relim(visible_only=True)
    ax.autoscale_view(True)
    line.set_data(x, y)
    ax.fill_between(x, -0.5, y, color="lightgrey")
    return (line,)


ani = animation.FuncAnimation(fig, animate, interval=300)
# ani.save("test.gif", writer='imagemagick', fps=10)
plt.show()
