#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import tkinter as tk
from center_window import center_window


app = tk.Tk()
app.title("entry_echo")
center_window(app)


def _on_key_press(event) -> None:
    text = entry.get()

    label_1["text"] = text
    label_2["text"] = text[::-1]


entry = tk.Entry(app)
entry.bind("<KeyRelease>", _on_key_press)
entry.pack()

label_1 = tk.Label(app)
label_1.pack()

label_2 = tk.Label(app)
label_2.pack()


app.mainloop()
