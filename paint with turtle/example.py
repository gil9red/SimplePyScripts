#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import turtle


turtle.color("red", "yellow")
turtle.begin_fill()

while True:
    turtle.forward(200)
    turtle.left(170)
    if abs(turtle.pos()) < 1:
        break

turtle.end_fill()
turtle.done()
