#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# https://docs.python.org/3/library/tkinter.html


import tkinter as tk
from tkinter import messagebox


def center_window(root, width=300, height=200) -> None:
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))


def on_btn_1() -> None:
    print("Hello World!")


def on_btn_2() -> None:
    text = "Hello World!"

    messagebox.showerror("Error", text)
    messagebox.showwarning("Warning", text)
    messagebox.showinfo("Information", text)


app = tk.Tk()
app.title("super_hello_world")
center_window(app)

label = tk.Label(app, text="Hello World!", font="Arial 16", fg="red")
label.pack()

btn_1 = tk.Button(app, text="Hello World!", command=on_btn_1)
btn_1.pack()

btn_2 = tk.Button(app, text="Click Me!", command=on_btn_2)
btn_2.pack()

app.mainloop()
