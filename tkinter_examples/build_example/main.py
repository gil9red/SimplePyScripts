#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Very very simple example of using the module tkinter.
# http://habrahabr.ru/post/151623/
from tkinter import *


tk = Tk()

text = StringVar()
name = StringVar()
name.set("HabrUser")
text.set("")
tk.title("MegaChat")
tk.geometry("400x300")

log = Text(tk)
nick = Entry(tk, textvariable=name)
msg = Entry(tk, textvariable=text)
msg.pack(side="bottom", fill="x", expand="true")
nick.pack(side="bottom", fill="x", expand="true")
log.pack(side="top", fill="both", expand="true")


def loopproc() -> None:
    print("Hello " + name.get() + "!")
    tk.after(1000, loopproc)


tk.after(1000, loopproc)
tk.mainloop()
