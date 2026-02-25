#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

city_map = list()

l, c = [int(i) for i in input().split()]
for i in range(l):
    row = input()
    print(row, file=sys.stderr)

    city_map.append(list(row))

print("city_map:", city_map, file=sys.stderr)

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

DIRECTION_DICT = {
    "SOUTH": (1, 0),
    "EAST": (0, 1),
    "NORTH": (-1, 0),
    "WEST": (0, -1),

    (1, 0): "SOUTH",
    (0, 1): "EAST",
    (-1, 0): "NORTH",
    (0, -1): "WEST",

    "S": "SOUTH",
    "E": "EAST",
    "N": "NORTH",
    "W": "WEST",
}


DEBUG = False


def log(*args, **kwargs) -> None:
    DEBUG and print(*args, **kwargs)


class Bender:
    def __init__(self, city_map) -> None:
        self.objects_map = dict()

        # Соберем все объекты на карте в словарь, исключаются пустые места и стенки
        for i in range(len(city_map)):
            row = city_map[i]
            for j in range(len(row)):
                cell = city_map[i][j]

                if cell == "@":
                    self.objects_map[cell] = i, j

                    # Под Бендером пустая клетка
                    self.objects_map[i, j] = " "
                else:
                    self.objects_map[i, j] = cell

        log("Objects map:", self.objects_map)
        log(f"Bender pos: {self.pos_i}x{self.pos_j}")

        self.direction_name = "SOUTH"

        self.invert = False
        self.breaker = False

        self.rows = len(city_map)
        self.cols = len(city_map[0])

        self.steps = list()
        # self.steps_log_list = list()

    def _set_pos_i(self, value) -> None:
        # Устанавливаем i, и старое j
        self.pos = value, self.pos[1]

    def _get_pos_i(self):
        return self.pos[0]

    pos_i = property(_get_pos_i, _set_pos_i)

    def _set_pos_j(self, value) -> None:
        # Устанавливаем старое i и j
        self.pos = self.pos[0], value

    def _get_pos_j(self):
        return self.pos[1]

    pos_j = property(_get_pos_j, _set_pos_j)

    def _set_pos(self, value) -> None:
        self.objects_map["@"] = value

    def _get_pos(self):
        return self.objects_map["@"]

    pos = property(_get_pos, _set_pos)

    def city_map(self):
        # Создаем карту
        map = list()
        for i in range(self.rows):
            row = [self.objects_map[i, j] for j in range(self.cols)]
            map.append(row)

        # Добавляем Бендера
        i, j = self.pos
        map[i][j] = "@"

        return map

    def print_city_map(self) -> None:
        log()
        for row in self.city_map():
            log(*row, sep="")
        log()

    def _set_direction_name(self, name) -> None:
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
            "SOUTH": self.objects_map[self.pos_i + 1, self.pos_j],
            "EAST": self.objects_map[self.pos_i, self.pos_j + 1],
            "NORTH": self.objects_map[self.pos_i - 1, self.pos_j],
            "WEST": self.objects_map[self.pos_i, self.pos_j - 1],
        }

    def step(self):
        self.print_city_map()

        log("Objects map:", self.objects_map)
        look_around = self.look_around()
        log(f"look_around: {look_around} {self.pos_i}x{self.pos_j}")
        log("Current direction:", self.direction_name)

        # Приоритеты смены движения при встрече с препятствием:
        # invert=False: SOUTH -> EAST  -> NORTH -> WEST
        # invert=True:  WEST  -> NORTH -> EAST  -> SOUTH
        priorities = ["SOUTH", "EAST", "NORTH", "WEST"]
        if self.invert:
            priorities.reverse()

        log("Current priorities:", priorities)
        priorities.remove(self.direction_name)

        while look_around:
            next_cell = look_around.pop(self.direction_name)
            log(f'while look_around: {self.direction_name} "{next_cell}" {look_around}')

            # Если следующий шаг не в препятствие, или препятствие и Бендер в режиме breaker
            if next_cell not in ["#", "X"] or (next_cell == "X" and self.breaker):
                break

            new_direction_name = priorities.pop(0)
            log(f"look_around change direction: {self.direction_name} -> {new_direction_name}.")
            self.direction_name = new_direction_name

        di, dj = self.get_direction(self.direction_name)

        self.pos_i += di
        self.pos_j += dj

        # Ломаем препятствие
        if next_cell == "X" and self.breaker:
            self.objects_map[self.pos] = " "

        current_cell = self.objects_map[self.pos]

        step = self.direction_name
        self.steps.append(step)

        # Проверяем, что наступили на изменение шага
        if current_cell in ["S", "E", "N", "W"]:
            # Указываем следующее направление движения
            self.direction_name = DIRECTION_DICT[current_cell]

        # Если попали на инвертирование приоритетов
        elif current_cell == "I":
            self.invert = not self.invert

        # Если нашли пиво
        elif current_cell == "B":
            self.breaker = not self.breaker
            log("breaker:", self.breaker)

        # Если нашли телепорт
        elif current_cell == "T":
            # Найдем положение другого телепорта
            other_teleport_pos = [
                k for k, v in self.objects_map.items() if v == "T" and k != self.pos
            ][0]
            log(f"teleport: {self.pos} -> {other_teleport_pos}")

            # Телепортируемся
            self.pos = other_teleport_pos

        return current_cell


bender = Bender(city_map)

# hack for LOOP
max_step_number = 200

steps = [
    "LOOP",
]

# Ходим, пока не встретим символ '$'
while True:
    max_step_number -= 1
    if max_step_number <= 0:
        break

    if bender.step() == "$":
        steps = bender.steps
        break

print("\n".join(steps))
