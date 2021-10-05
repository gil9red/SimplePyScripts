#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import itertools
import tkinter as tk


root = tk.Tk()
root.geometry('200x200')


CYCLED_IMAGES = itertools.cycle([
    tk.PhotoImage(file="icons/ok.png"),
    tk.PhotoImage(file="icons/no.png"),
    tk.PhotoImage(file="icons/help.png"),
])


def get_next_image() -> tk.PhotoImage:
    return next(CYCLED_IMAGES)


def _on_button_click():
    panel.config(image=get_next_image())


panel = tk.Label(root, image=get_next_image())
panel.pack()

button = tk.Button(root, text="ClickMe!")
button.config(command=lambda: _on_button_click())
button.pack()

root.mainloop()
