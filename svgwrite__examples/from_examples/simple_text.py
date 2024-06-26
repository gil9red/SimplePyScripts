#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/mozman/svgwrite/blob/master/examples/simple_text.py


# pip install svgwrite
import svgwrite


def simple_text(name):
    dwg = svgwrite.Drawing(name, (200, 200), debug=True)

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
    atext.add(dwg.tspan(" Word", font_size="1.5em", fill="red"))
    atext.add(dwg.tspan(" is a Word!", dy=["1em"], font_size="0.7em", fill="green"))
    paragraph.add(dwg.text("Das ist ein Test mit ÖÄÜäüö!", (10, 120)))
    paragraph.add(atext)

    dwg.save()


if __name__ == "__main__":
    import sys

    prog_name = sys.argv[0].rstrip(".py") + ".svg"

    simple_text(prog_name)
