#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from tkinter import Tk, Frame, Label
from tkinter import BOTH, Listbox, StringVar, END


class Example(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Listbox")
        self.pack(fill=BOTH, expand=1)

        acts = ['Scarlett Johansson', 'Rachel Weiss', 'Natalie Portman', 'Jessica Alba']

        lb = Listbox(self)
        for i in acts:
            lb.insert(END, i)

        lb.bind("<<ListboxSelect>>", self.on_select)

        lb.pack(pady=15)

        self.var = StringVar()
        self.label = Label(self, text=0, textvariable=self.var)
        self.label.pack()

    def on_select(self, val):
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)

        self.var.set(value)


if __name__ == '__main__':
    root = Tk()
    ex = Example(root)
    root.geometry("300x250+300+300")
    root.mainloop()
