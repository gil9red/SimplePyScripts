#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import tkinter as tk


class Example(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.button = tk.Button(self, text="Append", command=self.on_click)
        self.button.pack()

        self.pack()

    def on_click(self):
        print("Hello World!")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Example")
    ex = Example(root)
    root.geometry("300x250+300+300")
    root.mainloop()
