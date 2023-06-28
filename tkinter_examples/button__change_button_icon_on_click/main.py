#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import tkinter as tk


def _on_button_click(button):
    global PHOTO_COUNTER
    PHOTO_COUNTER += 1
    if len(photo_list) <= PHOTO_COUNTER:
        PHOTO_COUNTER = 0

    button.config(image=photo_list[PHOTO_COUNTER])


root = tk.Tk()
root.geometry("200x200")

PHOTO_COUNTER = 0

photo_list = [
    tk.PhotoImage(file="icons/ok.png"),
    tk.PhotoImage(file="icons/no.png"),
    tk.PhotoImage(file="icons/help.png"),
]

button = tk.Button(root, text="ClickMe!", image=photo_list[PHOTO_COUNTER])
button.config(command=lambda: _on_button_click(button))
button.pack()

root.mainloop()
