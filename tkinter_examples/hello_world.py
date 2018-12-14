#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# https://docs.python.org/3/library/tkinter.html


import tkinter as tk


class Application(tk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.QUIT = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        self.QUIT.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(parent=root)
    app.mainloop()
