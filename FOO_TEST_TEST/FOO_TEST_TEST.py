#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/mozman/svgwrite


# pip install svgwrite
import svgwrite


dwg = svgwrite.Drawing('test.svg', (200, 200), debug=True)
paragraph = dwg.add(dwg.g(font_size=14))
paragraph.add(dwg.text("This is a Test!", (10, 20)))
# 'x', 'y', 'dx', 'dy' and 'rotate' has to be a <list> or a <tuple>!!!
# 'param'[0] .. first letter, 'param'[1] .. second letter, and so on
# if there are more letters than values, the last list-value is used
#
# different 'y' coordinates does not work with Firefox 3.6
paragraph.add(dwg.text("This is a Test", x=[10], y=[40, 45, 50, 55, 60]))

# different formats can be used by the TSpan element
# The atext.tspan(...) method is a shortcut for: atext.add(dwg.tspan(...))
atext = dwg.text("A", insert=(10, 80), style="text-shadow: 2px 2px;")

# text color is set by the 'fill' property and 'stroke sets the outline color.
atext.add(dwg.tspan(' Word', font_size='1.5em', fill='red'))
atext.add(dwg.tspan(' is a Word!', dy=['1em'], font_size='0.7em', fill='green'))
paragraph.add(dwg.text("Das ist ein Test mit ÖÄÜäüö!", (10, 120)))
paragraph.add(atext)
dwg.save()


# dwg = svgwrite.Drawing('test.svg', profile='tiny')
# print(dwg.text)
# # dwg.add(dwg.line((0, 0), (10, 0), stroke=svgwrite.rgb(10, 10, 16, '%')))
# # dwg.add(dwg.text('Test', insert=(0, 0.2), fill='red'))
# dwg.add(dwg.text('Test', insert=(0, 0), fill='black'))
# dwg.save()
