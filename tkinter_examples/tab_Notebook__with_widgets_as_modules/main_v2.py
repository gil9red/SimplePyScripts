#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from tkinter import ttk, Tk

from tab_a import Example as TabA
from tab_b import Example as TabB
from tab_c import Example as TabC


class MainInterface:
    def __init__(self) -> None:
        self.window = Tk()
        self.window.title("version")
        self.window.geometry("300x250")
        self.create_widgets()

    def create_widgets(self) -> None:
        self.window["padx"] = 10
        self.window["pady"] = 10

        self.notebook = ttk.Notebook(self.window, width=1000, height=700)

        a_tab = TabA(self.notebook)
        b_tab = TabB(self.notebook)
        c_tab = TabC(self.notebook)

        self.notebook.add(a_tab, text="Notebook A")
        self.notebook.add(b_tab, text="Notebook B")
        self.notebook.add(c_tab, text="Notebook C")

        self.notebook.pack()


if __name__ == "__main__":
    program = MainInterface()
    program.window.mainloop()
