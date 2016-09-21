#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

city_map = list()

l, c = [int(i) for i in input().split()]
for i in range(l):
    row = input()
    print(row, file=sys.stderr)

    city_map.append(list(row))

print('city_map:', city_map, file=sys.stderr)

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

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


DEBUG = False


def log(*args, **kwargs):
    DEBUG and print(*args, **kwargs)


class Bender:
    def __init__(self, city_map):
        self.objects_map = dict()

        # Соберем все объекты на карте в словарь, исключаются пустые места и стенки
        for i in range(len(city_map)):
            row = city_map[i]
            for j in range(len(row)):
                cell = city_map[i][j]

                if cell == '@':
                    self.objects_map[cell] = i, j

                    # Под Бендером пустая клетка
                    self.objects_map[i, j] = ' '
                else:
                    self.objects_map[i, j] = cell

        log('Objects map:', self.objects_map)
        log('Bender pos: {}x{}'.format(self.pos_i, self.pos_j))

        self.direction_name = 'SOUTH'

        self.invert = False
        self.breaker = False

        self.rows = len(city_map)
        self.cols = len(city_map[0])

        self.steps = list()
        # self.steps_log_list = list()

    def _set_pos_i(self, value):
        # Устанавливаем i, и старое j
        self.pos = value, self.pos[1]

    def _get_pos_i(self):
        return self.pos[0]

    pos_i = property(_get_pos_i, _set_pos_i)

    def _set_pos_j(self, value):
        # Устанавливаем старое i и j
        self.pos = self.pos[0], value

    def _get_pos_j(self):
        return self.pos[1]

    pos_j = property(_get_pos_j, _set_pos_j)

    def _set_pos(self, value):
        self.objects_map['@'] = value

    def _get_pos(self):
        return self.objects_map['@']

    pos = property(_get_pos, _set_pos)

    def city_map(self):
        # Создаем карту
        map = list()
        for i in range(self.rows):
            row = [self.objects_map[i, j] for j in range(self.cols)]
            map.append(row)

        # Добавляем Бендера
        i, j = self.pos
        map[i][j] = '@'

        return map

    def print_city_map(self):
        log()
        for row in self.city_map():
            log(*row, sep='')
        log()

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
            'SOUTH': self.objects_map[self.pos_i + 1, self.pos_j],
            'EAST': self.objects_map[self.pos_i, self.pos_j + 1],
            'NORTH': self.objects_map[self.pos_i - 1, self.pos_j],
            'WEST': self.objects_map[self.pos_i, self.pos_j - 1],
        }

    def step(self):
        self.print_city_map()

        log('Objects map:', self.objects_map)
        look_around = self.look_around()
        log("look_around: {} {}x{}".format(look_around, self.pos_i, self.pos_j))
        log('Current direction:', self.direction_name)

        # Приоритеты смены движения при встрече с препятствием:
        # invert=False: SOUTH -> EAST  -> NORTH -> WEST
        # invert=True:  WEST  -> NORTH -> EAST  -> SOUTH
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

            new_direction_name = priorities.pop(0)
            log('look_around change direction: {} -> {}.'.format(self.direction_name, new_direction_name))
            self.direction_name = new_direction_name

        di, dj = self.get_direction(self.direction_name)

        self.pos_i += di
        self.pos_j += dj

        # Ломаем препятствие
        if next_cell == 'X' and self.breaker:
            self.objects_map[self.pos] = ' '

        current_cell = self.objects_map[self.pos]

        # TODO: проверка на зацикленность
        # Если по скорости, то дополнительная хэш таблица, в котрой будут храниться все посещенные объекты.
        # Если по памяти, то есть классический алгоритм, когда по списку пускаем 2 указателя, один за шаг переходит на 1 элемент вперед,
        # 2-й - на 2 элемента вперед. При проходе 2-м проверяем, если он указывает на тот-же объект, что и первый - значит цикл есть.
        #
        # точно
        #
        # class Item
        #     {
        #         public Item Next { get; set;}
        #         public bool HasLoop()
        #         {
        #             Item c = this;
        #             Item f = c.Next;
        #             while (c != null && f != null && f.Next != null)
        #             {
        #                 c = c.Next;
        #                 f = f.Next.Next;
        #                 if (c == f) return true;
        #             }
        #             return false;
        #         }
        #     }
        #
        # vik_tor,
        # 1) Строим матрицу смежности для графа.
        # 2) Проверяем диагонали графа, если отлично от 0, значит есть цикл.
        # 3) Возводим матрицу смежности в степень 2,3,4... и переходим к пп 2, пока матрица не станет нулевой.
        #
        # step = (self.direction_name, self.pos)
        # if step in self.steps:
        #     return 'LOOP'
        #
        # Алгоритм следующий:
        # 1) Каждый элемент списка помещаем в нашу обертку, одним из полей которой будет являться ThreadLocal переменная - флаг. Изначально флаг выключен.
        # 2) Когда мы посещаем элемент, поднимаем флаг.
        # 3) Если нашли поднятый флаг - список зациклен. Если уперлись в next==null - нет.
        #
        # Нельзя проверить   зацикленность  многопоточно поскольку это в любом случае не атомарная операция.
        # Придется делать доступ до метода синхронизированным. И дальше можно:
        # 1. Сделать фиктивный флаг для каждого node что мы тут уже были
        # 2. Пустить два итератора. Первый по правилу i=i+1, второй по правилу i=i+2. И если второй догонит первый, то у вас есть цикл.
        # 3. Вариант с удалением ссылок на next.
        #
        #
        #
        #
        # Ведем учет состояния Бендера и если оно повторяется, мы зациклены
        # step_log = self.direction_name, self.pos, self.invert, self.breaker
        # if step_log in self.steps_log_list:
        #     return 'LOOP'
        #
        # self.steps_log_list.append(step_log)
        #
        #

        step = self.direction_name
        self.steps.append(step)

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

        # Если нашли телепорт
        elif current_cell == 'T':
            # Найдем положение другого телепорта
            other_teleport_pos = [k for k, v in self.objects_map.items() if v == 'T' and k != self.pos][0]
            log('teleport: {} -> {}'.format(self.pos, other_teleport_pos))

            # Телепортируемся
            self.pos = other_teleport_pos

        return current_cell


bender = Bender(city_map)

# hack for LOOP
max_step_number = 200

steps = ['LOOP']

# Ходим, пока не встретим символ '$'
while True:
    max_step_number -= 1
    if max_step_number <= 0:
        break

    if bender.step() == '$':
        steps = bender.steps
        break

print('\n'.join(steps))
