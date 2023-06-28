#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import base64
import sys
import tkinter as tk

import requests

sys.path.append("..")
from center_window import center_window


# Download image and convert to base64
url = "https://www.python.org/static/img/python-logo.png"
img_data = requests.get(url).content
img_base64_data = base64.b64encode(img_data)

app = tk.Tk()
app.title("Label Image")
center_window(app)

image = tk.PhotoImage(data=img_base64_data)
label_image = tk.Label(app, image=image)
label_image.pack()

app.mainloop()
