#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import cydoomgeneric as cdg
from demopygame import PygameDoom


g = PygameDoom()
cdg.init(
    g._resx,
    g._resy,
    g.draw_frame,
    g.get_key,
    set_window_title=g.set_window_title,
)
cdg.main(argv=["cydoomgeneric", "-iwad", "DOOM1.WAD"])
