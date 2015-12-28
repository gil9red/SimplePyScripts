#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from enum import Enum
from collections import defaultdict


from common import get_logger
logger = get_logger('played_games_parser')


class Parser:
    """Класс парсера. Содержит словарь платформ и объект неопределенных игр."""

    class CategoryEnum(Enum):
        """Перечисление видов категории."""

        # Четыре ниже используется для идентификации игр и платформ
        # OTHER -- только для идентифакации игр, т.к. у неопределенных игр нет категорий
        FINISHED_GAME = 0
        NOT_FINISHED_GAME = 1
        FINISHED_WATCHED = 2
        NOT_FINISHED_WATCHED = 3
        OTHER = 4

        # @classmethod
        # def fromstring(cls, str):
        #     try:
        #         return getattr(cls, str.upper())
        #     except AttributeError:
        #         return None

    class Game:
        """Класс игры. Содержит название игры и категорию, в которую игра входит."""

        def __init__(self, name=None, category=None):
            self.name = name
            self.category = category

        @property
        def category_kind(self):
            return self.category.kind if self.category is not None else None

        def __str__(self):
            return '"{}"'.format(self.name)

        def __repr__(self):
            return self.__str__()

    # TODO: Сделать итериуремой! TypeError: 'Category' object is not iterable
    class Category:
        """Класс категории. Содержит список игр, входящих в данную категорию."""

        def __init__(self, kind=None):
            self.kind = kind
            self.game_list = set()

        def add(self, name):
            self.game_list.add(Parser.Game(name, self.kind))

    class Platform:
        """Класс платформы. Содержит название, словарь категорий платформы и список всех игр платформы."""

        def __init__(self, name=None):
            self.name = name
            self.categories = dict()
            # self.game_list = set()

        # TODO: заполнять во время парсинга
        @property
        def game_list(self):
            games = set()

            # Добавляем все игры категории
            for v in self.categories.values():
                games.update(v.game_list)

            return games

        def get(self, kind_category):
            if kind_category not in self.categories:
                category = Parser.Category(kind_category)
                self.categories[kind_category] = category
                return category

            return self.categories[kind_category]

            # # Пытаемся преобразовать атрибут в перечисление, иначе пытаемся получить
            # # как атрибут
            # kind = Parser.CategoryEnum.fromstring(kind_category)
            # if kind is not None:
            #     if kind not in self.categories:
            #         category = Parser.Category(kind)
            #         self.categories[kind] = category
            #         return category
            #
            #     return self.categories[kind]
            #
            # return None

    class Other:
        """Класс неопределенных игр. Содержит словарь платформ."""

        def __init__(self):
            self.platforms = dict()

        def add(self, name_platform, name_game):
            # Получаем платформу, создаем категорию и добавляем в нее игру
            self.get(name_platform).get(Parser.CategoryEnum.OTHER).add(name_game)

        def get(self, name_platform):
            if name_platform not in self.platforms:
                platform = Parser.Platform(name_platform)
                self.platforms[name_platform] = platform
                return platform

            return self.platforms[name_platform]

    def __init__(self):
        self.platforms = dict()
        self.other = Parser.Other()

    def get(self, name_platform):
        if name_platform not in self.platforms:
            platform = Parser.Platform(name_platform)
            self.platforms[name_platform] = platform
            return platform

        return self.platforms[name_platform]

    def parse(self, text):
        self.platforms.clear()
        self.other.platforms.clear()

        for line in text.split('\n'):
            line = line.rstrip()
            if not line:
                continue

            # Определим игровую платформу: ПК, консоли и т.п.
            if (line[0] not in [' ', '-', '@'] and line[0] not in [' ', '-', '@']) and line.endswith(':'):
                # Имя платформы без двоеточия на конце
                name_platform = line[0: len(line) - 1]
                platform_item = self.get(name_platform)
                continue

            if name_platform:
                # Первые 2 символа -- тэг игры: пройденная, не пройденная, просмотренная
                attributes = line[0:2]

                # Проверим на неизвестные атрибуты
                unknown_attributes = str(attributes)
                for c in ' -@':
                    unknown_attributes = unknown_attributes.replace(c, '')

                # Если строка не пуста, значит в ней есть неизвестные символы
                if unknown_attributes:
                    # Добавляем, если нет, к неопределенным играм узел платформы или получаем платформу
                    logger.warning('Обнаружен неизвестный атрибут: {}, игра: {}, платформа: '.format(
                        unknown_attributes, line, name_platform))
                    self.other.add(name_platform, line)
                    continue

                # TODO: рефакторинг
                is_finished_watched = attributes == '@ ' or attributes == ' @'
                is_not_finished_watched = attributes == '@-' or attributes == '-@'

                is_finished_game = attributes == '  '
                is_not_finished_game = attributes == '- ' or attributes == ' -'

                game_name = line[2:]

                if is_finished_game:
                    platform_item.get(Parser.CategoryEnum.FINISHED_GAME).add(game_name)
                elif is_not_finished_game:
                    platform_item.get(Parser.CategoryEnum.NOT_FINISHED_GAME).add(game_name)
                elif is_finished_watched:
                    platform_item.get(Parser.CategoryEnum.FINISHED_WATCHED).add(game_name)
                elif is_not_finished_watched:
                    platform_item.get(Parser.CategoryEnum.NOT_FINISHED_WATCHED).add(game_name)
                else:
                    logger.warning('Неопределенная игра {}, платформа: {}.'.format(line, name_platform))
                    self.other.add(name_platform, game_name)


if __name__ == '__main__':
    text = open('gistfile1.txt', encoding='utf8').read()

    p = Parser()
    p.parse(text)

    # TODO: отсортировать платформы по количеству игр в них

    print()
    # TODO: количество считать во время парсига
    print('Platforms ({}):'.format(sum([len(p.game_list) for p in p.platforms.values()])))
    for k, v in p.platforms.items():
        print('{}{}({}):'.format(' ' * 4, k, len(v.game_list)))

        for kind, category in v.categories.items():
            print('{}{}({}):'.format(' ' * 4 * 2, kind, len(category.game_list)))

            for game in category.game_list:
                print(' ' * 4 * 3, game)

            print()

        print()

    print()
    # TODO: количество считать во время парсига
    print('Other ({}):'.format(sum([len(p.game_list) for p in p.other.platforms.values()])))
    for k, v in p.other.platforms.items():
        print('{}{}({}):'.format(' ' * 4, k, len(v.game_list)))

        for game in v.game_list:
            print(' ' * 4 * 2 + str(game))
