#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE:   https://github.com/mozman/svgwrite
# DOC:      https://svgwrite.readthedocs.io/en/master/
# EXAMPLES: https://github.com/mozman/svgwrite/tree/master/examples


# pip install svgwrite
import svgwrite


dwg = svgwrite.Drawing("hello_world.svg")

paragraph = dwg.add(dwg.g(font_size=20))
paragraph.add(dwg.text("Hello World!", (5, 20)))
paragraph.add(dwg.text("Привет Мир!", (5, 40)))

dwg.save()
