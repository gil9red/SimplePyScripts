#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from tkinter import *


root = Tk()
root.title("Шашки")

canvas = Canvas(root, width=700, height=700)
canvas.pack()


def square() -> None:
    y = 0
    while y < 700:
        x = 0
        while x < 700:
            canvas.create_rectangle(x, y, x + 88, y + 88, fill="#fff", outline="#000")
            x += 88

        y += 88


def board() -> None:
    fill = "#FECD72"
    outline = "#825100"
    for i in range(0, 8):
        for j in range(0, 8):
            x1, y1, x2, y2 = i * 88, j * 88, i * 88 + 88, j * 88 + 88
            canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=outline)

            fill, outline = outline, fill

        fill, outline = outline, fill


def checkers() -> None:
    board = [
        [0, 2, 0, 2, 0, 2, 0, 2],
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 2, 0, 2, 0, 2, 0, 2],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
    ]

    outline = "#000"

    for i in range(8):
        for j in range(8):
            value = board[i][j]
            if value == 0:
                continue

            color = "white" if value == 1 else "black"

            x1, y1, x2, y2 = j * 88, i * 88, j * 88 + 88, i * 88 + 88
            canvas.create_oval(x1, y1, x2, y2, fill=color, outline=outline)


square()
board()
checkers()

root.mainloop()
