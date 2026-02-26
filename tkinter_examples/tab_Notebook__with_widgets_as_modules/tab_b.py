#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import tkinter as tk


class Example(tk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.parent = parent
        self.init_ui()

    def init_ui(self) -> None:
        self.text = tk.Text(self, width=20, height=10)
        self.text.pack()
        self.text.insert(1.0, "Hello World!\nFoo\nBar\n\n123\n")

        self.button = tk.Button(self, text="Append", command=self.on_append)
        self.button.pack()

        self.pack()

    def on_append(self) -> None:
        self.text.insert(tk.END, "Go-go-go!\n")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Example")
    ex = Example(root)
    root.geometry("300x250+300+300")
    root.mainloop()
