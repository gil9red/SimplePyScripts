#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

surface_n = int(input())  # the number of points used to draw the surface of Mars.
for i in range(surface_n):
    # land_x: X coordinate of a surface point. (0 to 6999)
    # land_y: Y coordinate of a surface point. By linking all the points together in a sequential fashion, you form the surface of Mars.
    land_x, land_y = [int(j) for j in input().split()]
    # print("land_x={}, land_y={}".format(land_x, land_y), file=sys.stderr)


# game loop
while True:
    # h_speed: the horizontal speed (in m/s), can be negative.
    # v_speed: the vertical speed (in m/s), can be negative.
    # fuel: the quantity of remaining fuel in liters.
    # rotate: the rotation angle in degrees (-90 to 90).
    # power: the thrust power (0 to 4).
    x, y, h_speed, v_speed, fuel, rotate, power = [int(i) for i in input().split()]
    print(
        f"x={x}, y={y}, h_speed={h_speed}, v_speed={v_speed}, fuel={fuel}, rotate={rotate}, power={power}",
        file=sys.stderr,
    )

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # 2 integers: rotate power. rotate is the desired rotation angle
    # (should be 0 for level 1), power is the desired thrust power (0 to 4).
    if v_speed < -40:
        print("0 4")
    else:
        print("0 2")
