#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""

  The Goal

Bender is a depressed robot who heals his depression by partying and drinking alcohol. To save him from a life of debauchery, his creators have reprogrammed the control system with a more rudimentary intelligence. Unfortunately, he has lost his sense of humor and his former friends have now rejected him.

Bender is now all alone and is wandering through the streets of Futurama with the intention of ending it all in a suicide booth.

To intercept him and save him from almost certain death, the authorities have given you a mission: write a program that will make it possible to foresee the path that Bender follows. To do so, you are given the logic for the new intelligence with which Bender has been programmed as well as a map of the city.
  Rules

The 9 rules of the new Bender system:

    Bender starts from the place indicated by the @ symbol on the map and heads SOUTH.
    Bender finishes his journey and dies when he reaches the suicide booth marked $.
    Obstacles that Bender may encounter are represented by # or X.
    When Bender encounters an obstacle, he changes direction using the following priorities: SOUTH, EAST, NORTH and WEST. So he first tries to go SOUTH, if he cannot, then he will go EAST, if he still cannot, then he will go NORTH, and finally if he still cannot, then he will go WEST.
    Along the way, Bender may come across path modifiers that will instantaneously make him change direction. The S modifier will make him turn SOUTH from then on, E, to the EAST, N to the NORTH and W to the WEST.
    The circuit inverters (I on map) produce a magnetic field which will reverse the direction priorities that Bender should choose when encountering an obstacle. Priorities will become WEST, NORTH, EAST, SOUTH. If Bender returns to an inverter I, then priorities are reset to their original state (SOUTH, EAST, NORTH, WEST).
    Bender can also find a few beers along his path (B on the map) that will give him strength and put him in “Breaker” mode. Breaker mode allows Bender to destroy and automatically pass through the obstacles represented by the character X (only the obstacles X). When an obstacle is destroyed, it remains so permanently and Bender maintains his course of direction. If Bender is in Breaker mode and passes over a beer again, then he immediately goes out of Breaker mode. The beers remain in place after Bender has passed.
    2 teleporters T may be present in the city. If Bender passes over a teleporter, then he is automatically teleported to the position of the other teleporter and he retains his direction and Breaker mode properties.
    Finally, the space characters are blank areas on the map (no special behavior other than those specified above).

Your program must display the sequence of moves taken by Bender according to the map provided as input.

The map is divided into lines (L) and columns (C). The contours of the map are always unbreakable # obstacles. The map always has a starting point @ and a suicide booth $.

If Bender cannot reach the suicide booth because he is indefinitely looping, then your program must only display LOOP.
  Example

Let the map below:
######
#@E $#
# N  #
#X   #
######

In this example, Bender will follow this sequence of moves:

    SOUTH (initial direction)
    EAST (because of the obstacle X)
    NORTH (change of direction caused by N)
    EAST (change of direction caused by E)
    EAST (current direction, until end point $)

  Game Input
Input

Line 1: the number of lines L and columns C on the map, separated by a space.

The following L lines: a line of the length C representing a line on the map. A line can contain the characters #, X, @, $, S, E, N, W, B, I, T and space character.
Output

    If Bender can reach $, then display the sequence of moves he has taken. One move per line: SOUTH for the South, EAST for the East, NORTH for the North and WEST for the west.
    If Bender cannot reach $, then only display LOOP.

Constraints
4 ≤ C ≤ 100
4 ≤ L ≤ 100

Example
Input

10 10
##########
#        #
#  S   W #
#        #
#  $     #
#        #
#@       #
#        #
#E     N #
##########

Output

SOUTH
SOUTH
EAST
EAST
EAST
EAST
EAST
EAST
NORTH
NORTH
NORTH
NORTH
NORTH
NORTH
WEST
WEST
WEST
WEST
SOUTH
SOUTH

"""


DIRECTION_DICT = {
    'SOUTH': (1, 0),
    'EAST': (0, 1),
    'NORTH': (-1, 0),
    'WEST': (0, -1),

    (1, 0): 'SOUTH',
    (0, 1): 'EAST',
    (-1, 0): 'NORTH',
    (0, -1): 'WEST',

    'S': 'SOUTH',
    'E': 'EAST',
    'N': 'NORTH',
    'W': 'WEST',
}


DEBUG = True


def log(*args, **kwargs):
    DEBUG and print(*args, **kwargs)


class Bender:
    def __init__(self, city_map):
        # Определим положение Бендера на карте
        for i in range(len(city_map)):
            row = city_map[i]
            for j in range(len(row)):
                if city_map[i][j] == '@':
                    self.pos_i, self.pos_j = i, j

        log('Bender pos: {}x{}'.format(self.pos_i, self.pos_j))

        self.direction_name = 'SOUTH'

        self.invert = False
        self.breaker = False

        # Пиво должно оставаться после того как его Бендер подберет
        # поэтому заводим флаг, который вернет пиво, после того как Бендер пройдет на следующую ячейку
        self.__previous_step_was_beer = False

        self.city_map = city_map
        self.steps = list()

    def _set_direction_name(self, name):
        self._direction_name = name

    def _get_direction_name(self):
        return self._direction_name

    direction_name = property(_get_direction_name, _set_direction_name)

    @property
    def direction(self):
        return self.get_direction(self.direction_name)

    @staticmethod
    def get_direction(direction_name):
        return DIRECTION_DICT[direction_name]

    def look_around(self):
        return {
            'SOUTH': self.city_map[self.pos_i + 1][self.pos_j],
            'EAST': self.city_map[self.pos_i][self.pos_j + 1],
            'NORTH': self.city_map[self.pos_i - 1][self.pos_j],
            'WEST': self.city_map[self.pos_i][self.pos_j - 1],
        }

    def step(self):
        log()
        for row in self.city_map:
            log(*row, sep='')
        log()

        look_around = self.look_around()
        log("look_around: {} {}x{}".format(look_around, self.pos_i, self.pos_j))
        log('Current direction:', self.direction_name)

        # Приоритеты смены движения при встрече с препятствием:
        # SOUTH -> EAST -> NORTH -> WEST -> SOUTH
        # WEST -> NORTH -> EAST -> SOUTH -> WEST
        priorities = ['SOUTH', 'EAST', 'NORTH', 'WEST']
        if self.invert:
            priorities.reverse()

        log('Current priorities:', priorities)
        priorities.remove(self.direction_name)

        while look_around:
            next_cell = look_around.pop(self.direction_name)
            log('while look_around: {} "{}" {}'.format(self.direction_name, next_cell, look_around))

            # Если следующий шаг не в препятствие, или препятствие и Бендер в режиме breaker
            if next_cell not in ['#', 'X'] or (next_cell == 'X' and self.breaker):
                break

            # new_direction_name = CHANGE_DIRECTION_DICT[(priorities.pop(0), self.invert)]
            new_direction_name = priorities.pop(0)
            log('look_around change direction: {} -> {}.'.format(self.direction_name, new_direction_name))
            self.direction_name = new_direction_name

        di, dj = self.get_direction(self.direction_name)

        if self.__previous_step_was_beer:
            self.__previous_step_was_beer = False

            # Пиво должно остаться на месте
            self.city_map[self.pos_i][self.pos_j] = 'B'

        else:
            self.city_map[self.pos_i][self.pos_j] = ' '

        self.pos_i += di
        self.pos_j += dj
        current_cell = self.city_map[self.pos_i][self.pos_j]

        # Перемещаем Бендера
        self.city_map[self.pos_i][self.pos_j] = '@'

        self.steps.append(self.direction_name)

        # Проверяем, что наступили на изменение шага
        if current_cell in ['S', 'E', 'N', 'W']:
            # Указываем следующее направление движения
            self.direction_name = DIRECTION_DICT[current_cell]

        # Если попали на инвертирование приоритетов
        elif current_cell == 'I':
            self.invert = not self.invert

        # Если нашли пиво
        elif current_cell == 'B':
            self.breaker = not self.breaker
            log('breaker:', self.breaker)

            self.__previous_step_was_beer = True

        return current_cell
