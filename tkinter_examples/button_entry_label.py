#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import tkinter as tk


def on_button_perevod_clicked() -> None:
    your_text = text1.get()
    a = your_text.encode("cp1251")
    b = list(map(int, a))
    for i in range(len(b)):
        if b[i] < 100:
            b[i] = "0" + str(b[i])

    label_info["text"] = b


root = tk.Tk()
text1 = tk.StringVar()

button_perevod = tk.Button(root, text="perevod", command=on_button_perevod_clicked)
entry_info = tk.Entry(root, textvariable=text1)
label_info = tk.Label(root, text="")

button_perevod.pack()
entry_info.pack()
label_info.pack()

root.mainloop()
