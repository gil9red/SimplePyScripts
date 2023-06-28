#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.stackoverflow.com/a/818915


import tkinter as tk
from math import cos, sin


root = tk.Tk()
root.geometry("760x710")

canv = tk.Canvas(root, width=700, height=700, bg="white")
canv.place(x=0, y=0)

k = 15
r = 15
t = 0.0


def but(event):
    global t

    for _ in range(100):
        x = r * (k - 1) * (cos(t) + (cos((k - 1) * t)) / (k - 1))
        y = r * (k - 1) * (sin(t) - (sin((k - 1) * t)) / (k - 1))
        canv.create_oval(x - 5 + 355, y - 5 + 355, x + 5 + 355, y + 5 + 355, fill="red")

        t += 0.1


button1 = tk.Button(
    root, text="start", width=3, height=4, bg="gold", fg="black", font=10
)
button1.place(x=720, y=355)
button1.bind("<Button-1>", but)

root.mainloop()
