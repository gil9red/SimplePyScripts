#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import tkinter as tk


def _on_button_click(button):
    button.config(image=get_next_image())


def next_image_generator():
    photo_list = [
        tk.PhotoImage(file="icons/ok.png"),
        tk.PhotoImage(file="icons/no.png"),
        tk.PhotoImage(file="icons/help.png"),
    ]

    while True:
        yield from photo_list


NEXT_IMAGE = next_image_generator()


def get_next_image():
    return next(NEXT_IMAGE)


root = tk.Tk()
root.geometry("200x200")

button = tk.Button(root, text="ClickMe!", image=get_next_image())
button.config(command=lambda: _on_button_click(button))
button.pack()

root.mainloop()
