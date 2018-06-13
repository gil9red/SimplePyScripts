#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/mozman/svgwrite/blob/master/examples/LSystem.py


# pip install svgwrite
import svgwrite

import math


LevyDragon = {'length':1, 'numAngle':4, 'level':16, 'init': 'FX',
              'target': 'X', 'replacement': 'X+YF+', 'target2': 'Y',
              'replacement2': '-FX-Y'}

KochSnowflake = {'length':1, 'numAngle':6, 'level':6, 'init': 'F++F++F',
                 'target': 'F', 'replacement': 'F-F++F-F', 'target2': '',
                 'replacement2': ''}

LevyCurve = {'length':1, 'numAngle':8, 'level':17, 'init': 'F',
             'target': 'F', 'replacement': '+F--F+', 'target2': '',
             'replacement2': ''}

HilbertSpaceFillingCurve = {'length':1, 'numAngle':4, 'level':5, 'init': 'L',
             'target': 'L', 'replacement': '+RF-LFL-FR+', 'target2': 'R',
             'replacement2': '-LF+RFR+FL-'}


# SOURCE: http://code.activestate.com/recipes/577159/
def LSystem(name, formula=LevyCurve):
    # L-System Fractals
    # FB - 201003276
    # image size

    # Generate the fractal drawing string
    def _LSystem(formula):
        state = formula['init']
        target = formula['target']
        replacement = formula['replacement']
        target2 = formula['target2']
        replacement2 = formula['replacement2']
        level = formula['level']

        for counter in range(level):
            state2 = ''
            for character in state:
                if character == target:
                    state2 += replacement
                elif character == target2:
                    state2 += replacement2
                else:
                    state2 += character

            state = state2

        return state

    print("Creating: %s\n" % name)
    xmin, ymin = (100000, 100000)
    xmax, ymax = (-100000, -100000)

    num_angle = formula['numAngle']
    length = formula['length']
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
    curve = dwg.polyline(points=[(x, y)], stroke='green', fill='none', stroke_width=0.1)

    for ch in fractal:
        if ch == 'F':
            # turtle forward(length)
            x += length * cs[k]
            y += length * sn[k]

            curve.points.append( (x, y) )

            # find maxima
            xmin = min(xmin, x)
            xmax = max(xmax, x)
            ymin = min(ymin, y)
            ymax = max(ymax, y)

        elif ch == '+':
            # turtle right(angle)
            k = (k + 1) % num_angle

        elif ch == '-':
            # turtle left(angle)
            k = ((k - 1) + num_angle) % num_angle

    print("L-System with %d segments.\n" % (len(curve.points) - 1))

    dwg.viewbox(xmin, ymin, xmax-xmin, ymax-ymin)
    dwg.add(curve)

    dwg.save()


if __name__ == '__main__':
    import sys
    prog_name = sys.argv[0].rstrip('.py')

    LSystem(prog_name + '__hilbert_space_filling_curve.svg', formula=HilbertSpaceFillingCurve)
    LSystem(prog_name + '__levy_dragon.svg', formula=LevyDragon)
    LSystem(prog_name + '__levy_curve.svg', formula=LevyCurve)
    LSystem(prog_name + '__kochsnow_flake.svg', formula=KochSnowflake)
