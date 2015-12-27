#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys

from urllib.request import urlopen, urlretrieve
from urllib.parse import urljoin

from lxml import etree
from io import StringIO

from PySide.QtGui import *
from PySide.QtCore import *


import logging


def get_logger(name, file='log.txt', encoding='utf8'):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s[LINE:%(lineno)d] %(levelname)-8s %(message)s')

    if file is not None:
        fh = logging.FileHandler(file, encoding=encoding)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    return log


logger = get_logger('played_games')


DEFAULT_URL = 'https://gist.github.com/gil9red/2f80a34fb601cd685353'

# # TODO: временно
# PROGRESS_BAR = None

# TODO: автоматизировать обновление файла gist

# TODO: скрипт проверки необходимости обновления
# from urllib.request import urlopen
# from lxml import etree
# from io import StringIO
# from datetime import datetime
#
#
# def need_update(local_last_update_datetime):
#     url = 'https://gist.github.com/gil9red/2f80a34fb601cd685353/revisions?diff=unified'
#
#     with urlopen(url) as f:
#         context = f.read().decode()
#
#     parser = etree.HTMLParser()
#     tree = etree.parse(StringIO(context), parser)
#
#     last_datetime = tree.xpath('//*[@class="gist-revision"]//time/@datetime')[0]
#     last_datetime = datetime.strptime(str(last_datetime), "%Y-%m-%dT%H:%M:%SZ")
#     print('last_datetime = ' + str(last_datetime))
#     print('local_last_update_datetime = ' + str(local_last_update_datetime))
#
#     return last_datetime > local_last_update_datetime
#
#
# local_last_update_datetime = datetime(2015, 12, 23)
# need = need_update(local_last_update_datetime)
# print('need_update = ' + str(need))


def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        if percent > 100:
            percent = 100
            readsofar = totalsize

        s = "\r%5.1f%% %*d / %d" % (percent, len(str(totalsize)), readsofar, totalsize)
        print(s, end='')
        # PROGRESS_BAR.setValue(percent)

        # near the end
        if readsofar >= totalsize:
            print()

    # total size is unknown
    else:
        print("read {}".format(readsofar))

    # TODO: не помогает
    app.processEvents()


ENUM_OFFSET = QTreeWidgetItem.UserType
ENUM_PLATFORM = ENUM_OFFSET + 1
ENUM_CATEGORY = ENUM_OFFSET + 2
ENUM_GAME = ENUM_OFFSET + 3
ENUM_OTHER = ENUM_OFFSET + 4
ENUM_OTHER_PLATFORM = ENUM_OFFSET + 5
ENUM_OTHER_GAME = ENUM_OFFSET + 6

TEST_USING_FILE_GAMES = False


TREE_HEADER = 'Games'


FINISHED_GAME_TITLE = 'Пройденные'
NOT_FINISHED_GAME_TITLE = 'Не закончено прохождение'
FINISHED_WATCHED_TITLE = 'Просмотренные'
NOT_FINISHED_WATCHED_TITLE = 'Не закончен просмотр'
OTHER_GAME_TITLE = 'Неопределенные игры'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Played Games')

        self.tree_games = QTreeWidget()

        self.line_edit_url = QLineEdit(DEFAULT_URL)
        self.button_refresh_by_url = QPushButton('&Refresh')
        self.button_refresh_by_url.clicked.connect(self.refresh_by_url)

        layout = QHBoxLayout()
        layout.addWidget(self.line_edit_url)
        layout.addWidget(self.button_refresh_by_url)

        self.line_edit_filter = QLineEdit('*')
        self.line_edit_filter.textEdited.connect(self.filter_games)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel('Filter:'))
        filter_layout.addWidget(self.line_edit_filter)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.tree_games)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

        # # TODO: временно
        # # self.progress_bar = QProgressBar()
        # # self.statusBar().addWidget(self.progress_bar)
        # global PROGRESS_BAR
        # PROGRESS_BAR = QProgressBar()
        # self.statusBar().addWidget(PROGRESS_BAR)

        # TODO: может, лучше на лету составлять список так же как и platform_list
        self.category_list = set()
        self.game_list = set()
        self.filtered_game_list = set()

        # Узел неопределенных игр
        self.strange_games = None

        self.update_header_tree()

    @property
    def platform_list(self):
        root = self.tree_games.invisibleRootItem()
        return [item for item in self.to_list_item(root) if item is not self.strange_games]

    @staticmethod
    def to_list_item(node):
        if node is None:
            # Чтобы не загромождать проверками на None или исключения. Если вернуть None, то в
            # в циклах, использующих эту функцию будут исключения: "TypeError: 'NoneType' object is not iterable"
            return list()

        return [node.child(i) for i in range(node.childCount())]

    def filter_games(self, filter_exp):
        logger.debug('Filter game start. filter_exp="{}".'.format(filter_exp))

        # Для возможности поиска просто по словам:
        if not filter_exp.endswith('*'):
            filter_exp += '*'
            logger.debug('Change filter_exp="{}".'.format(filter_exp))

        # Очищаем множество. Добавляем в него отфильтрованные игры. Удаляем элементы, не входящие в множество игры.
        self.filtered_game_list.clear()
        self.filtered_game_list.update(set(self.tree_games.findItems(filter_exp, Qt.MatchRecursive | Qt.MatchWildcard)))
        self.filtered_game_list.intersection_update(self.game_list)
        logger.debug('Filter game finish. Games: {}.'.format(len(self.filtered_game_list)))

        logger.debug('Tree update start.')

        # Прячем не прошедшие фильтрацию игры, а также категории и платформы, если их дети все спрятаны.
        logger.debug('Hide game: {}.'.format(self.hide_games()))
        logger.debug('Hide categories: {}.'.format(self.hide_nodes(self.category_list)))
        logger.debug('Hide platform: {}.'.format(self.hide_nodes(self.platform_list)))

        if self.strange_games is not None:
            logger.debug('Hide strange category: {}.'.format(self.hide_nodes(self.to_list_item(self.strange_games))))
            logger.debug('Hide strange: {}.'.format(self.hide_node(self.strange_games)))

        logger.debug('Tree update finish.')

        self.update_header_tree()

    def hide_games(self):
        count = 0

        # Если элемента нет в отфильтрованном списке, прячем его
        for item in self.game_list:
            if item not in self.filtered_game_list:
                item.setHidden(True)
                count += 1
            else:
                item.setHidden(False)

        return count

    def hide_node(self, node):
        """Функция скрывает те узлы, у которых всех дети скрыты, иначе -- показывает."""

        if node is None:
            return

        def all_hidden(self, node):
            for item in self.to_list_item(node):
                if not item.isHidden():
                    return False

            return True

        is_hide = all_hidden(self, node)
        node.setHidden(is_hide)

        return is_hide

    def hide_nodes(self, nodes):
        # Подсчитаем сколько будет скрыто категорий
        count = 0
        for node in nodes:
            if self.hide_node(node):
                count += 1

        return count

    # TODO: выполнить функцию в другом потоке
    # def download(self, url):
    #     logger.debug('Download {} start.'.format(url))
    #     local_filename, headers = urlretrieve(url, reporthook=reporthook)
    #     logger.debug('Download finish:\nlocal_filename: {}\n\nHeaders:\n{}'.format(local_filename, headers))
    #
    #     logger.debug('Read from file start: ' + local_filename)
    #     with open(local_filename, encoding='utf-8') as f:
    #         content_file = f.read()
    #
    #     logger.debug('Read from file finish.')
    #
    #     logger.debug('Load tree start.')
    #     self.load_tree(content_file)
    #     logger.debug('Load tree finish.')
    #
    #     self.tree_games.expandAll()

    def refresh_by_url(self):
        # TODO: выполнить функцию в другом потоке
        # TODO: после окончания рабоыт потока генерировать сигнал
        # и в нем вернуть путь к файлу
        # import threading
        #
        # thread = threading.Thread(target=self.download, args=(self.line_edit_url.text(),))
        # thread.start()
        # thread.join()

        logger.debug('TEST_USING_FILE_GAMES=' + str(TEST_USING_FILE_GAMES))

        if TEST_USING_FILE_GAMES:
            # TODO: для тестирования интерфейса
            content_file = open('gistfile1.txt', 'r', encoding='utf8').read()
        else:
            # PROGRESS_BAR.show()
            # PROGRESS_BAR.setValue(-1)

            url = self.line_edit_url.text()

            # Теперь нужно получить url файла с последней ревизией
            logger.debug('Get url file last revision start.')

            with urlopen(url) as f:
                context = f.read().decode()

                parser = etree.HTMLParser()
                tree = etree.parse(StringIO(context), parser)

                rel_url = tree.xpath('//*[@class="btn btn-sm "]/@href')[0]
                logger.debug('Relative url = {}.'.format(rel_url))

                url = urljoin(url, str(rel_url))
                logger.debug('Full url = {}.'.format(url))

            logger.debug('Get url file last revision finish.')

            logger.debug('Download {} start.'.format(url))
            local_filename, headers = urlretrieve(url, reporthook=reporthook)
            logger.debug('Download finish:\nlocal_filename: {}\n\nHeaders:\n{}'.format(local_filename, headers))

            # # Через 3 секунды прячем прогресс бар
            # QTimer.singleShot(5000, PROGRESS_BAR.hide)

            logger.debug('Read from file start: ' + local_filename)
            with open(local_filename, encoding='utf-8') as f:
                content_file = f.read()

        logger.debug('Read from file finish.')

        logger.debug('Load tree start.')
        self.load_tree(content_file)
        logger.debug('Load tree finish.')

        self.tree_games.expandAll()

        # from urllib.request import urlopen
        #
        # # TODO: избавить от подвисания программы во время загрузки файла и его парсинга
        # # TODO: В отдельном потоке
        # # TODO: прогресс загрузки из сети файла (хотя бы в процентах)
        # with urlopen(self.line_edit_url.text()) as f:
        #     self.load_tree(f.read().decode())
        #
        # TODO: кэширование
        # from urllib.request import urlretrieve
        # urlretrieve(self.line_edit_url.text(), 'gistfile1.txt')
        #
        # self.tree_games.expandAll()

    def load_tree(self, text):
        # TODO: сделать модель дерева
        self.tree_games.clear()
        self.game_list.clear()
        self.filtered_game_list.clear()

        # file_name = 'gistfile1.txt'

        # TODO: вынести парсер в отдельную функцию
        # platforms_game_dict = dict()
        platform = None

        platform_item = None
        finished_game_items = None
        not_finished_game_items = None
        finished_watched_items = None
        not_finished_watched_items = None

        self.strange_games = QTreeWidgetItem([OTHER_GAME_TITLE], ENUM_OTHER)
        strange_platform_games_dict = dict()

        # TODO: В узлах показывается количество детей, а не игр
        # TODO: добавить кнопку выбора удаления пустых узлов
        # TODO: кнопку показа статистики: игры, платформы
        # TODO: показывать в заголовке сколько всего игр найдено и платформ

        def delete_empty_category():
            """Удаление пустых узлов."""

            if platform_item is None:
                return

            if finished_game_items is not None and finished_game_items.childCount() == 0:
                platform_item.removeChild(finished_game_items)

            if not_finished_game_items is not None and not_finished_game_items.childCount() == 0:
                platform_item.removeChild(not_finished_game_items)

            if finished_watched_items is not None and finished_watched_items.childCount() == 0:
                platform_item.removeChild(finished_watched_items)

            if not_finished_watched_items is not None and not_finished_watched_items.childCount() == 0:
                platform_item.removeChild(not_finished_watched_items)

            # Добавление в множества оставшихся после удаления элементов категории
            for item in self.to_list_item(platform_item):
                self.category_list.add(item)

        def set_count_children_nodes(platform):
            """Функция добавляет к названиям узлов количество их детей"""

            def set_text(item, title, count=None):
                item.setText(0, '{} ({})'.format(title, item.childCount() if count is None else count))

            # TODO: какой-нибудь рекурсивный алгоритм справится изящнее
            # TODO: refactoring
            if platform_item is not None:
                platform_game_count = finished_game_items.childCount()
                set_text(finished_game_items, FINISHED_GAME_TITLE)

                platform_game_count += not_finished_game_items.childCount()
                set_text(not_finished_game_items, NOT_FINISHED_GAME_TITLE)

                platform_game_count += finished_watched_items.childCount()
                set_text(finished_watched_items, FINISHED_WATCHED_TITLE)

                platform_game_count += not_finished_watched_items.childCount()
                set_text(not_finished_watched_items, NOT_FINISHED_WATCHED_TITLE)

                set_text(platform_item, platform, platform_game_count)

        for line in text.split('\n'):
            # TODO: должно помочь от подвисания интерфейса
            app.processEvents()

            line = line.rstrip()

            if line:
                # TODO: рефакторинг
                # Определим игровую платформу: ПК, консоли и т.п.
                if (line[0] not in [' ', '-', '@'] and line[0] not in [' ', '-', '@']) and line.endswith(':'):
                    set_count_children_nodes(platform)
                    delete_empty_category()

                    # Имя платформы без двоеточия на конце
                    platform = line[0: len(line) - 1]
                    platform_item = QTreeWidgetItem([platform], ENUM_PLATFORM)
                    self.tree_games.addTopLevelItem(platform_item)

                    finished_game_items = QTreeWidgetItem([FINISHED_GAME_TITLE], ENUM_CATEGORY)
                    not_finished_game_items = QTreeWidgetItem([NOT_FINISHED_GAME_TITLE], ENUM_CATEGORY)
                    finished_watched_items = QTreeWidgetItem([FINISHED_WATCHED_TITLE], ENUM_CATEGORY)
                    not_finished_watched_items = QTreeWidgetItem([NOT_FINISHED_WATCHED_TITLE], ENUM_CATEGORY)

                    platform_item.addChild(finished_game_items)
                    platform_item.addChild(not_finished_game_items)
                    platform_item.addChild(finished_watched_items)
                    platform_item.addChild(not_finished_watched_items)
                    continue

                if platform:
                    # Первые 2 символа -- тэг игры: пройденная, не пройденная, просмотренная
                    attributes = line[0:2]

                    # Проверим на неизвестные атрибуты
                    unknown_attributes = str(attributes)
                    for c in ' -@':
                        unknown_attributes = unknown_attributes.replace(c, '')

                    # Если строка не пуста, значит в ней есть неизвестные символы
                    if unknown_attributes:
                        # Добавляем к неопределенным играм узел платформы
                        if platform not in strange_platform_games_dict:
                            strange_game_platform_item = QTreeWidgetItem([platform], ENUM_OTHER_PLATFORM)
                            strange_platform_games_dict[platform] = strange_game_platform_item
                            self.strange_games.addChild(strange_game_platform_item)
                        else:
                            strange_game_platform_item = strange_platform_games_dict[platform]

                        logger.warning('!!! Обнаружен неизвестный атрибут !!!: ' + unknown_attributes + ', игра: '
                                       + line + ', платформа: ' + platform)
                        game_item = QTreeWidgetItem([line], ENUM_GAME)
                        strange_game_platform_item.addChild(game_item)
                        self.game_list.add(game_item)
                        continue

                    # TODO: рефакторинг
                    is_finished_watched = attributes == '@ ' or attributes == ' @'
                    is_not_finished_watched = attributes == '@-' or attributes == '-@'

                    is_finished_game = attributes == '  '
                    is_not_finished_game = attributes == '- ' or attributes == ' -'

                    # TODO: rem
                    game_name = line[2:]
                    # platforms_game_dict[platform] = game_name

                    game_item = QTreeWidgetItem([game_name], ENUM_GAME)
                    self.game_list.add(game_item)
                    # platform_item.addChild(game_item)

                    if is_finished_game:
                        finished_game_items.addChild(game_item)
                    elif is_not_finished_game:
                        not_finished_game_items.addChild(game_item)
                    elif is_finished_watched:
                        finished_watched_items.addChild(game_item)
                    elif is_not_finished_watched:
                        not_finished_watched_items.addChild(game_item)
                    else:
                        logger.warning('!!! Неопределенная игра !!! ' + line + ', платформа: ' + platform)

                        # Добавляем к неопределенным играм узел платформы
                        if platform not in strange_platform_games_dict:
                            strange_game_platform_item = QTreeWidgetItem([platform], ENUM_OTHER_PLATFORM)
                            strange_platform_games_dict[platform] = strange_game_platform_item
                            self.strange_games.addChild(strange_game_platform_item)
                        else:
                            strange_game_platform_item = strange_platform_games_dict[platform]

                        game_item.setText(0, line + ' / ' + platform)
                        strange_game_platform_item.addChild(game_item)

        set_count_children_nodes(platform)
        delete_empty_category()

        # Добавляем узел неопределенных игр
        if self.strange_games.childCount() > 0:
            self.tree_games.addTopLevelItem(self.strange_games)
        else:
            self.strange_games = None

        # print(platforms_game_dict)

        # Указываем количество неопределенных игр в узле неопределенных игр и его детей-платформ
        count_other_game = 0

        for platform, platform_item in strange_platform_games_dict.items():
            platform_item.setText(0, '{} ({})'.format(platform, platform_item.childCount()))
            count_other_game += platform_item.childCount()

        if self.strange_games is not None:
            self.strange_games.setText(0, '{} ({})'.format(OTHER_GAME_TITLE, count_other_game))

        # Применяем фильтр к элементам
        self.filter_games(self.line_edit_filter.text())

        self.update_header_tree()

    def update_header_tree(self):
        # Проверяем, что фильтр какие-нибудь игры отфильтровал
        enabled_filter = len(self.game_list) != len(self.filtered_game_list)

        # Указываем в заголовке общее количество игр и при фильтр, количество игр, оставшихся после фильтрации
        self.tree_games.setHeaderLabel(
            '{} ({})'.format(TREE_HEADER, len(self.game_list)) +
            ('' if not enabled_filter else '. Filtered ' + str(len(self.filtered_game_list)))
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.show()
    mw.refresh_by_url()

    sys.exit(app.exec_())
