#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/mozman/svgwrite/blob/master/examples/LSystem.py
# DOC:    https://en.wikipedia.org/wiki/L-system


# pip install svgwrite
import svgwrite

import math


# https://en.wikipedia.org/wiki/L-system#Example_6:_Dragon_curve
DragonCurve = {
    "length": 1,
    "numAngle": 4,
    "level": 10,
    "init": "FX",
    "target": "X",
    "replacement": "X+YF+",
    "target2": "Y",
    "replacement2": "-FX-Y",
    "ignore": "XY",
}

KochSnowflake = {
    "length": 1,
    "numAngle": 6,
    "level": 6,
    "init": "F++F++F",
    "target": "F",
    "replacement": "F-F++F-F",
    "target2": "",
    "replacement2": "",
}

LevyCurve = {
    "length": 1,
    "numAngle": 8,
    "level": 12,
    "init": "F",
    "target": "F",
    "replacement": "+F--F+",
    "target2": "",
    "replacement2": "",
}

# https://en.wikipedia.org/wiki/Hilbert_curve#Representation_as_Lindenmayer_system
HilbertSpaceFillingCurve = {
    "length": 1,
    "numAngle": 4,
    "level": 5,
    "init": "A",
    "target": "A",
    "replacement": "-BF+AFA+FB-",
    "target2": "B",
    "replacement2": "+AF-BFB-FA+",
    "ignore": "AB",
}


# https://en.wikipedia.org/wiki/L-system#Example_5:_Sierpinski_triangle
SierpinskiTriangle = {
    "length": 1,
    "numAngle": 3,
    "level": 6,
    "init": "F-G-G",
    "target": "F",
    "replacement": "F-G+F+G-F",
    "target2": "G",
    "replacement2": "GG",
}

# https://en.wikipedia.org/wiki/L-system#Example_5:_Sierpinski_triangle
SierpinskiTriangleArrowheadCurve = {
    "length": 1,
    "numAngle": 6,
    "level": 6,
    "init": "A",
    "target": "A",
    "replacement": "B-A-B",
    "target2": "B",
    "replacement2": "A+B+A",
}

# https://en.wikipedia.org/wiki/L-system#Example_4:_Koch_curve
KochCurve = {
    "length": 1,
    "numAngle": 4,
    "level": 3,
    "init": "F",
    "target": "F",
    "replacement": "F+F-F-F+F",
    "target2": "",
    "replacement2": "",
}


# TODO: append "Fractal plant", "Cantor set", "Fractal (binary) tree"
#       https://en.wikipedia.org/wiki/L-system
#
# TODO: _LSystem -> support square bracket syntax, example:
#       https://en.wikipedia.org/wiki/L-system#Example_2:_Fractal_(binary)_tree
#       https://en.wikipedia.org/wiki/L-system#Example_7:_Fractal_plant


# SOURCE: http://code.activestate.com/recipes/577159/
def LSystem(name, formula=LevyCurve) -> None:
    # L-System Fractals

    print("Creating: " + name)

    # Generate the fractal drawing string
    def _LSystem(formula):
        state = formula["init"]
        target = formula["target"]
        replacement = formula["replacement"]
        target2 = formula["target2"]
        replacement2 = formula["replacement2"]
        level = formula["level"]

        for counter in range(level):
            state2 = ""
            for character in state:
                if character == target:
                    state2 += replacement
                elif character == target2:
                    state2 += replacement2
                else:
                    state2 += character

            state = state2

        return state

    xmin, ymin = (100000, 100000)
    xmax, ymax = (-100000, -100000)

    num_angle = formula["numAngle"]
    length = formula["length"]
    fractal = _LSystem(formula)
    na = 2.0 * math.pi / num_angle

    sn = []
    cs = []

    for i in range(num_angle):
        sn.append(math.sin(na * i))
        cs.append(math.cos(na * i))

    x = 0.0
    y = 0.0

    k = 0
    dwg = svgwrite.Drawing(name, debug=True)
    curve = dwg.polyline(points=[(x, y)], stroke="green", fill="none", stroke_width=0.1)

    for ch in fractal:
        # Ignore
        if formula.get("ignore") and ch in formula.get("ignore"):
            continue

        if ch == "+":
            # Turtle right(angle)
            k = (k + 1) % num_angle

        elif ch == "-":
            # Turtle left(angle)
            k = ((k - 1) + num_angle) % num_angle

        else:
            # Draw line

            # Turtle forward(length)
            x += length * cs[k]
            y += length * sn[k]

            curve.points.append((x, y))

            # Find maxima
            xmin = min(xmin, x)
            xmax = max(xmax, x)
            ymin = min(ymin, y)
            ymax = max(ymax, y)

    print("L-System with %d segments.\n" % (len(curve.points) - 1))

    dwg.viewbox(xmin, ymin, xmax - xmin, ymax - ymin)
    dwg.add(curve)

    dwg.save()


if __name__ == "__main__":
    import sys

    prog_name = sys.argv[0].rstrip(".py")

    LSystem(prog_name + "__dragon_curve.svg", formula=DragonCurve)
    LSystem(prog_name + "__kochsnow_snowflake.svg", formula=KochSnowflake)
    LSystem(prog_name + "__levy_curve.svg", formula=LevyCurve)
    LSystem(
        prog_name + "__hilbert_space_filling_curve.svg",
        formula=HilbertSpaceFillingCurve,
    )
    LSystem(prog_name + "__sierpinski_triangle.svg", formula=SierpinskiTriangle)
    LSystem(
        prog_name + "__sierpinski_triangle_arrowhead_curve.svg",
        formula=SierpinskiTriangleArrowheadCurve,
    )
    LSystem(prog_name + "__koch_curve.svg", formula=KochCurve)

    # # Loop for level step
    # for i in range(2, 5 + 1):
    #     formula = SierpinskiTriangle.copy()
    #     formula['level'] = i
    #     LSystem(prog_name + '__sierpinski_triangle__n{}.svg'.format(i), formula=formula)
