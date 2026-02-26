#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import tkinter as tk


def create_window() -> None:
    window = tk.Toplevel(root)

    button_new = tk.Button(window, text="Create new+ window", command=create_window)
    button_new.pack()

    button_close = tk.Button(window, text="Close", command=window.destroy)
    button_close.pack()


root = tk.Tk()
button = tk.Button(root, text="Create new window", command=create_window)
button.pack()

root.mainloop()
