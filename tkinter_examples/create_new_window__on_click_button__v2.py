#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from tkinter import Tk, Label, Button


class MainApp(Tk):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        label = Label(self, text="First Window")
        button = Button(self, text="Open Window", command=self.new_window)

        label.pack()
        button.pack()

    def new_window(self):
        Window().mainloop()


class Window(Tk):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        label = Label(self, text="Second Window")
        label.pack()


if __name__ == "__main__":
    MainApp().mainloop()
