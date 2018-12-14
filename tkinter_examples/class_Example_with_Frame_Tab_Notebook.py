#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import tkinter as tk
from tkinter import ttk


class Example(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.notebook = ttk.Notebook(self, width=1000, height=700)

        a_tab = ttk.Frame(self.notebook)
        b_tab = ttk.Frame(self.notebook)
        c_tab = ttk.Frame(self.notebook)

        self.notebook.add(a_tab, text="Notebook A")
        self.notebook.add(b_tab, text="Notebook B")
        self.notebook.add(c_tab, text="Notebook C")

        self.notebook.pack()
        self.pack()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Example')
    ex = Example(root)
    root.geometry("300x250+300+300")
    root.mainloop()
