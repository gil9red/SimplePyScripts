#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from tkinter import Tk, ttk
import tkinter as tk

from tab_a import Example as TabA
from tab_b import Example as TabB
from tab_c import Example as TabC


# class MainInterface:
#     def __init__(self):
#         self.window = tk.Tk()
#         self.window.title('version')
#         self.window.geometry("1024x768")
#         self.create_widgets()
#
#     def create_widgets(self):
#         self.window['padx'] = 10
#         self.window['pady'] = 10
#
#         self.notebook = ttk.Notebook(self.window, width=1000, height=700)
#
#         a_tab = TabA(self.notebook)
#         b_tab = TabB(self.notebook)
#         c_tab = TabC(self.notebook)
#
#         self.notebook.add(a_tab, text="Notebook A")
#         self.notebook.add(b_tab, text="Notebook B")
#         self.notebook.add(c_tab, text="Notebook C")
#
#         self.notebook.grid(row=1, column=1)
#
#
# if __name__ == '__main__':
#     program = MainInterface()
#     program.window.mainloop()

class MainWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.parent.title('version')

        self.init_ui()

    def init_ui(self):
        self.parent['padx'] = 10
        self.parent['pady'] = 10

        self.notebook = ttk.Notebook(self, width=1000, height=700)

        a_tab = TabA(self.notebook)
        b_tab = TabB(self.notebook)
        c_tab = TabC(self.notebook)

        self.notebook.add(a_tab, text="Notebook A")
        self.notebook.add(b_tab, text="Notebook B")
        self.notebook.add(c_tab, text="Notebook C")

        self.notebook.pack()

        self.pack()


if __name__ == '__main__':
    root = Tk()
    ex = MainWindow(root)
    root.geometry("300x250")
    root.mainloop()
