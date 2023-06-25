#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from graphics import *


win = GraphWin("My Circle", 100, 100)
c = Circle(Point(50, 50), 10)
c.draw(win)
win.getMouse()  # Pause to view result
win.close()
