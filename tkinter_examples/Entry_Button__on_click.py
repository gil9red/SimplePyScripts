#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from tkinter import *
from tkinter import messagebox


def on_button_clicked() -> None:
    try:
        w = int(weight.get())
        h = int(height.get())

    except ValueError:
        messagebox.showwarning(
            "Warning", "Поля вес и рост должны быть заполнены числами"
        )
        return

    print(w)
    print(h)


root = Tk()

label1 = Label(text="Введите вес (кг):")
weight = Entry(root)

label2 = Label(text="Введите рост (см):")
height = Entry(root)

button = Button(root, text="Ok", command=on_button_clicked)

label1.pack()
weight.pack()
label2.pack()
height.pack()
button.pack()

root.mainloop()
