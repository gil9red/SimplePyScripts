#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from tkinter import Tk, Label


def turn(event):
    value = event.widget["text"]
    value = 1 if value == "." else int(value) + 1

    event.widget["text"] = value


root = Tk()

for x in range(8):
    for y in range(8):
        cell = Label(root, width=3, height=1, text=".")
        cell.grid(row=x, column=y)
        cell.bind("<Button-1>", turn)

root.mainloop()
