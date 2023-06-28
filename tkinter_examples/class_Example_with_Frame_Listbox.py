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
        self.pack(fill=tk.BOTH, expand=1)

        acts = ["Scarlett Johansson", "Rachel Weiss", "Natalie Portman", "Jessica Alba"]

        self.lb = tk.Listbox(self)
        for i in acts:
            self.lb.insert(tk.END, i)
            self.lb.bind("<<ListboxSelect>>", self.on_select)
            self.lb.pack(pady=15)

        self.var = tk.StringVar()
        self.label = tk.Label(self, text=0, textvariable=self.var)
        self.label.pack()

        self.pack()

    def on_select(self, val):
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)

        self.var.set(value)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Example")
    ex = Example(root)
    root.geometry("300x250+300+300")
    root.mainloop()
