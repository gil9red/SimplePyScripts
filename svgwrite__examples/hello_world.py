#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/mozman/svgwrite


# pip install svgwrite
import svgwrite


dwg = svgwrite.Drawing('test.svg', (200, 200), debug=True)
paragraph = dwg.add(dwg.g(font_size=20))
paragraph.add(dwg.text("Hello World!", (5, 20)))
paragraph.add(dwg.text("Привет Мир!", (5, 40)))

dwg.save()
