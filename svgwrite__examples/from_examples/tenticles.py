#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/mozman/svgwrite/blob/master/examples/ltattrie/tenticles.py


# pip install svgwrite
import svgwrite

import math
import random


def gen_colour(start_p, end_p, n_p):
    """
    gen_colour generates a list of colours from start to end. Colours are linearly interpreted between start and end.
    start and end must be (int, int, int), n integer is how many colours are to be generated.
    """
    c_start = start_p
    c_end = end_p
    n = n_p

    # yielding a c_end separately gives the exact c_end thus not something that is 99.99% c_
    # end which is slightly off colour.
    for i in range(n):
        ccolour = (
            int(c_start[0] + (float(i) / float(n)) * (c_end[0] - c_start[0])),
            int(c_start[1] + (float(i) / float(n)) * (c_end[1] - c_start[1])),
            int(c_start[2] + (float(i) / float(n)) * (c_end[2] - c_start[2])),
        )
        yield ccolour

    yield c_end


def gen_incr_num():
    i = 0
    while True:
        i += 1
        yield i


UNIQUE_NUM = gen_incr_num()


class Tendrile:
    def __init__(
        self,
        p_x,
        p_y,
        p_width,
        p_angle,
        p_step,
        p_v,
        p_curl,
        p_n,
        p_scolour,
        p_ecolour,
        p_can_branch,
        dwg,
    ) -> None:
        """tendrile class instance for each arm"""
        self.x = p_x
        self.y = p_y
        self.width = p_width

        self.angle_set(p_angle)  # limit value of angle
        self.step = p_step
        self.v = p_v
        self.curl = p_curl
        self.n = p_n  # length of tendrile
        self.scolour = p_scolour  # starting colour
        self.ecolour = p_ecolour  # ending colour
        self.can_branch = p_can_branch  # Can tendrile branch?
        self.stroke_width = 1
        self.lin_colour = gen_colour(self.scolour, self.ecolour, self.n)
        self.r = self.width

        self.dwg = dwg

        # The purpose of having a group for all of the circles is be able to add all of the circles
        # of a tendrile to the drawing at the same time. If a tendrile branches, creating a new
        # tendrile the new tendrile will be drawn completely before the older tendrile is drawn.
        # This puts the new tendrile in the background and the old tendrile in front.  When the
        # program had been written to start writting the old tendrile, write the new tendrile, then
        # finish the old tendrile there was a problem that slivers of some of the new tendrile's
        # colour was over top of the old tendrile causing a confusing mix of colour.
        # Using a group does create a small problem. The whole new tendrile is in the background of
        # the whole old tendrile. This is not perspectively correct because if a old tendrile
        # branches near the end of the tendrile the new tendrile should be in front of any part of
        # of the beginning part of the old tendrile but instead the new tendrile will be behind all
        # of the old tendrile.
        self.group = self.dwg.g(id="branch" + str(next(UNIQUE_NUM)))

    def angle_set(self, p_val) -> None:
        # limit the angle to range -2*math.pi to 2*math.pi  which is +- full circle.
        # Use math.fmod because % returns with the sign of the second number.
        self.angle = math.fmod(p_val, (2 * math.pi))

    def create(self) -> None:
        for i in range(self.n):
            if i != 0:
                if random.randint(1, 100) == 1 and self.can_branch:
                    distance = (
                        self.r * 0.8
                    )  # The new circle is % of the previouse circle's width
                    x_temp = self.x + math.cos(self.angle) * distance
                    y_temp = self.y + math.sin(self.angle) * distance

                    v_delta_split = math.pi / 31.4  # .05 degrees

                    self.v = (
                        self.v + v_delta_split + random.uniform(-self.step, self.step)
                    )
                    self.v *= 0.9 + self.curl * 0.1

                    self.angle_set(self.angle + self.v)  # limit value of angle

                    # Create the tendrile
                    # The use of the original colour, usually darker green, to start the new tendrile
                    # gives a slight look of shadow on the the start of the new tendrile. It also gives a clear visual
                    # separation between the existing tendrile and the new tendrile.
                    tend = Tendrile(
                        x_temp,
                        y_temp,
                        self.r,
                        self.angle,
                        (self.step * 1.2),
                        (-1.0 * self.v),
                        self.curl,
                        (self.n - i - 1),
                        self.scolour,
                        self.ecolour,
                        False,
                        self.dwg,
                    )

                    # Create the tendrile as svg elements
                    tend.create()

                    # Draw the tendrile as svg elements
                    tend.draw()

                    self.x += math.cos(self.angle) * distance
                    self.y += math.sin(self.angle) * distance

                    # Set up angle for next circle
                    self.v += random.uniform(-self.step, self.step)
                    self.v *= 0.9 + self.curl * 0.1
                    self.angle_set(self.angle + self.v)  # limit value of angle

                else:
                    distance = (
                        self.r * 0.8
                    )  # The new circle is % of the previouse circle's width
                    self.x += math.cos(self.angle) * distance
                    self.y += math.sin(self.angle) * distance

                    self.v += random.uniform(-self.step, self.step)
                    self.v *= 0.9 + self.curl * 0.1

                    self.angle_set(self.angle + self.v)  # limit value of angle

            self.r = (
                1 - float(i) / self.n
            ) * self.width  # radius size gradually decreases.

            new_colour = next(self.lin_colour)
            stroke_colour = "rgb(%s,%s,%s)" % new_colour
            fill_colour = "rgb(%s,%s,%s)" % new_colour
            self.group.add(
                self.dwg.circle(
                    center=(self.x, self.y),
                    r=self.r,
                    fill=fill_colour,
                    stroke=stroke_colour,
                    stroke_width=3,
                )
            )

    def draw(self) -> None:
        self.dwg.add(self.group)


def create_svg(name) -> None:
    """
    Create many circles in a curling tentril fashion.
    """

    svg_size_width = 900
    svg_size_height = 900

    dwg = svgwrite.Drawing(name, (svg_size_width, svg_size_height), debug=True)

    # Background will be black so the background does not overwhelm the colors.
    dwg.add(
        dwg.rect(insert=(0, 0), size=("100%", "100%"), rx=None, ry=None, fill="black")
    )

    # Create effect instance and apply it.
    # option values.
    n = 100  # number of circles default 100

    num_arms = 5  # number of tendriles default 5

    d_width = svg_size_width
    d_height = svg_size_height

    step = 4.0 / n

    # Starting colour. Colour will linearly change to ending colour.
    green_light1 = (102, 229, 132)
    green_dark1 = (25, 76, 37)

    # starting colour. Colour will linearly change to ending colour.
    start_colour = green_dark1
    end_colour = green_light1

    # n         - number of circles in each tendrile.
    # num_arms  - number of arms that is tendriles.
    # x, y     - centre of current circle, 0,0 is top left of screen
    # c_width  - initial circle width.
    # r        - radius of current circle. gradually decreases.
    # distance - length to next circle.
    # angle    - angle to next circle. value -pi to +pi.
    # step     - range of randomness of angle. constant.
    # curl     - how much curl will happen. constant. .1*curl incremented to v, angle.
    # v        - change in angle. random value -step to +step plus curl
    # can_branch - true or false. Can this tendrile branch?
    can_branch = True

    ###########################
    # The change in the starting colour is small so all of the tenticles seem like a group but
    # still have a very slight variation to give individuality. If the starting colour is too
    # different the arms look like they are not connected at the centre.
    start_lin_colour = gen_colour(start_colour, end_colour, num_arms * 8)

    # Create all tendriles
    for j in range(num_arms):
        # Set start of arm x y
        x = d_height / 2
        y = d_width / 2
        angle = random.uniform(
            (-1.0 * math.pi), math.pi
        )  # random angle in radians. 2*pi radians = 360 degrees
        v = 0.0

        # Variety to the size of the starting circle
        c_width = random.uniform((d_width * 0.015), (d_width * 0.025))
        r = random.uniform((c_width * 0.9), (c_width * 1.1))
        new_start_colour = next(start_lin_colour)

        curl = 1.0

        # Create a tendrile
        tend = Tendrile(
            x,
            y,
            r,
            angle,
            step,
            v,
            curl,
            n,
            new_start_colour,
            end_colour,
            can_branch,
            dwg,
        )

        # Create the tendrile as svg elements
        tend.create()

        # Draw the tendrile as svg elements
        tend.draw()

    dwg.save()


if __name__ == "__main__":
    import sys

    prog_name = sys.argv[0].rstrip(".py") + ".svg"

    create_svg(prog_name)
