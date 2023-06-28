#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def center_window(root, width=300, height=200):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))


if __name__ == "__main__":
    import tkinter as tk

    app = tk.Tk()
    app.title("center_window")
    center_window(app)

    label = tk.Label(app, text="Hello World!", font="Arial 16", fg="red")
    label.pack()

    app.mainloop()
