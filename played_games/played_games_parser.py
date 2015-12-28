#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from enum import Enum

from common import get_logger
logger = get_logger('played_games_parser')


# TODO: ОПТИМИЗАЦИЯ: Подсчет количества детей делать во время парсинга
# TODO: Попытаться при разборе игры определить, что в ней написана последовательность серий игры


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

    class Game:
        """Класс игры. Содержит название игры и категорию, в которую игра входит."""

        def __init__(self, name=None, category=None):
            self.name = name
            self.category = category

        @property
        def category_kind(self):
            return self.category.kind if self.category is not None else None

        def __str__(self):
            return 'Game "{}" ({})'.format(self.name, self.category_kind)

        def __repr__(self):
            return self.__str__()

    class Category:
        """Класс категории. Содержит список игр, входящих в данную категорию.
        Итерируемый класс, в цикле возвращает игры.

        """

        def __init__(self, kind=None, platform=None):
            self.kind = kind
            self.game_list = list()
            self.platform = platform

        @property
        def count(self):
            """Свойство возвращает количество игр в категории."""

            return len(self.game_list)

        def add(self, name):
            self.game_list.append(Parser.Game(name, self))

        def __iter__(self):
            return self.game_list.__iter__()

        def next(self):
            return self.game_list.next()

        def __str__(self):
            return 'Category {} ({})'.format(self.kind, self.count)

        def __repr__(self):
            return self.__str__()

    class Platform:
        """Класс платформы. Содержит название, словарь категорий платформы и список
        всех игр платформы.

        """

        def __init__(self, name=None):
            self.name = name
            self.categories = dict()

        @property
        def count_games(self):
            return len(self.game_list)

        @property
        def count_categories(self):
            return len(self.categories)

        @property
        def game_list(self):
            games = set()

            # Добавляем все игры категории
            for v in self.categories.values():
                games.update(v.game_list)

            return frozenset(games)

        def get(self, kind_category):
            if kind_category not in self.categories:
                category = Parser.Category(kind_category, self)
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

        def __str__(self):
            return 'Platform {}. Games: {}. Categories: {}.'.format(self.name, self.count_games, self.count_categories)

        def __repr__(self):
            return self.__str__()

    class Other:
        """Класс неопределенных игр. Содержит словарь платформ."""

        def __init__(self):
            self.platforms = dict()

        @property
        def count_games(self):
            return sum([p.count_games for p in self.platforms.values()])

        @property
        def count_platforms(self):
            return len(self.platforms)

        def add_game(self, name_platform, name_game):
            # Получаем платформу, создаем категорию и добавляем в нее игру
            self.get(name_platform).get(Parser.CategoryEnum.OTHER).add(name_game)

        def get(self, name_platform):
            """Функция возращает ссылку на объект Платформа. Если платформа с таким именем
            не существует, она будет будет создана.

            """

            if name_platform not in self.platforms:
                platform = Parser.Platform(name_platform)
                self.platforms[name_platform] = platform
                return platform

            return self.platforms[name_platform]

        def __str__(self):
            return 'Other. Platforms: {}. Games: {}. '.format(self.count_platforms, self.count_categories)

        def __repr__(self):
            return self.__str__()

    ALL_ATTRIBUTES_GAMES = ' -@'

    def __init__(self):
        self.platforms = dict()
        self.other = Parser.Other()

    @property
    def count_games(self):
        return sum([p.count_games for p in p.platforms.values()])

    @property
    def count_platforms(self):
        return len(self.platforms)

    def get(self, name_platform):
        """Функция возращает ссылку на объект Платформа. Если платформа с таким именем
        не существует, она будет будет создана.

        """

        if name_platform not in self.platforms:
            platform = Parser.Platform(name_platform)
            self.platforms[name_platform] = platform
            return platform

        return self.platforms[name_platform]

    def parse(self, text):
        self.platforms.clear()
        self.other.platforms.clear()

        name_platform = None

        # Проходим в текст построчно
        for line in text.split('\n'):
            line = line.rstrip()
            if not line:
                continue

            # Определим игровую платформу: ПК, консоли и т.п.
            if (line[0] not in Parser.ALL_ATTRIBUTES_GAMES and
                        line[0] not in Parser.ALL_ATTRIBUTES_GAMES) and line.endswith(':'):
                # Имя платформы без двоеточия на конце
                name_platform = line[0: len(line) - 1]
                platform_item = self.get(name_platform)
                continue

            if name_platform:
                # Первые 2 символа -- тэг игры: пройденная, не пройденная, просмотренная
                attributes = line[0:2]

                # Проверим на неизвестные атрибуты
                unknown_attributes = str(attributes)
                for c in Parser.ALL_ATTRIBUTES_GAMES:
                    unknown_attributes = unknown_attributes.replace(c, '')

                # Если строка не пуста, значит в ней есть неизвестные символы
                if unknown_attributes:
                    # Добавляем, если нет, к неопределенным играм узел платформы или получаем платформу
                    logger.warning('Обнаружен неизвестный атрибут: {}, игра: {}, платформа: '.format(
                        unknown_attributes, line, name_platform))
                    self.other.add_game(name_platform, line)
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
                    self.other.add_game(name_platform, game_name)

        # TODO: Сделать сортировку настраиваемой. Напрмиер, хранить два списка: обычный,
        # который был заполнен при парсинге и производный от него -- отсортированный
        # Сортировка игр
        for platform in self.platforms.values():
            for category in platform.categories.values():
                category.game_list.sort(key=lambda x: x.name, reverse=False)

        for platform in self.other.platforms.values():
            for category in platform.categories.values():
                category.game_list.sort(key=lambda x: x.name, reverse=False)

    @property
    def sorted_platforms(self, reverse=True):
        """Возвращает отсортированный список кортежей (имя_платформы, платформа).
        Сортируется по количеству игр в платформе.

        """

        return sorted(p.platforms.items(), key=lambda x: x[1].count_games, reverse=reverse)


if __name__ == '__main__':
    text = open('gistfile1.txt', encoding='utf8').read()

    p = Parser()
    p.parse(text)

    indent = ' ' * 2

    print()
    print('Games ({})'.format(p.count_games))
    print('Platforms ({}):'.format(p.count_platforms))
    for k, v in p.sorted_platforms:
        print('{}{}({}):'.format(indent, k, v.count_games))

        for kind, category in v.categories.items():
            print('{}{}({}):'.format(indent * 2, kind, category.count))

            for game in category:
                print(indent * 3, game.name)

            print()

    print()
    print('Other ({}/{}):'.format(p.other.count_platforms, p.other.count_games))
    for k, v in p.other.platforms.items():
        print('{}{}({}):'.format(indent, k, v.count_games))

        for category in v.categories.values():
            for game in category:
                print(indent * 2 + game.name)
