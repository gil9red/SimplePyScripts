#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from tkinter import *


root = Tk()
root.title("Chess board")

canvas = Canvas(root, width=700, height=700, bg="#fff")
canvas.pack()

fill = "#fff"
outline = "#000"
size = 88

for i in range(8):
    for j in range(8):
        x1, y1, x2, y2 = i * size, j * size, i * size + size, j * size + size

        canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=outline)
        fill, outline = outline, fill

    fill, outline = outline, fill

root.mainloop()
