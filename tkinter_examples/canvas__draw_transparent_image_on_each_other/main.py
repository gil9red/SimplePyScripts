#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import tkinter as tk


root = tk.Tk()
canvas = tk.Canvas(root, width=200, height=200, bg="white")
image_sky = tk.PhotoImage(file="text.png")
image_sun = tk.PhotoImage(file="stars.png")
canvas.create_image(0, 0, image=image_sky, anchor=tk.NW)
canvas.create_image(0, 0, image=image_sun, anchor=tk.NW)
canvas.pack()
root.mainloop()
