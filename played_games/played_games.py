#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

import sys
import os
from urllib.request import urlretrieve

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


DEFAULT_URL = 'https://gist.githubusercontent.com/gil9red/2f80a34fb601cd685353/raw/f0d8086ae9053f389db02aca6eecb4e53ab4d034/gistfile1.txt'

# # TODO: временно
# PROGRESS_BAR = None


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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Played Games')

        self.tree_games = QTreeWidget()
        self.tree_games.setHeaderLabel('Games')

        self.line_edit_url = QLineEdit(DEFAULT_URL)
        self.button_refresh_by_url = QPushButton('&Refresh')
        self.button_refresh_by_url.clicked.connect(self.refresh_by_url)

        layout = QHBoxLayout()
        layout.addWidget(self.line_edit_url)
        layout.addWidget(self.button_refresh_by_url)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
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

        url = self.line_edit_url.text()

        # # TODO: для тестирования интерфейса
        # content_file = open('gistfile1.txt', 'r').read()

        # PROGRESS_BAR.show()
        # PROGRESS_BAR.setValue(-1)

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
        self.tree_games.clear()

        # file_name = 'gistfile1.txt'

        # TODO: вынести парсер в отдельную функцию
        # platforms_game_dict = dict()
        platform = None

        platform_item = None
        finished_game_items = None
        not_finished_game_items = None
        finished_watched_items = None
        not_finished_watched_items = None

        strange_games = QTreeWidgetItem(['Неопределенных игры'])
        strange_platform_games_dict = dict()

        # TODO: В узлах показывается количество детей, а не игр
        # TODO: добавить кнопку выбора удаления пустых узлов
        # TODO: кнопку показа статистики: игры, платформы
        # TODO: показывать в заголовке сколько всего игр найдено и платформ

        def delete_empty_nodes():
            """Удаление пустых узлов."""

            if finished_game_items is not None and finished_game_items.childCount() == 0:
                finished_game_items.parent().removeChild(finished_game_items)

            if not_finished_game_items is not None and not_finished_game_items.childCount() == 0:
                not_finished_game_items.parent().removeChild(not_finished_game_items)

            if finished_watched_items is not None and finished_watched_items.childCount() == 0:
                finished_watched_items.parent().removeChild(finished_watched_items)

            if not_finished_watched_items is not None and not_finished_watched_items.childCount() == 0:
                not_finished_watched_items.parent().removeChild(not_finished_watched_items)

        FINISHED_GAME_TITLE = 'Пройденные'
        NOT_FINISHED_GAME_TITLE = 'Не закончено прохождение'
        FINISHED_WATCHED_TITLE = 'Просмотренные'
        NOT_FINISHED_WATCHED_TITLE = 'Не закончен просмотр'

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

    # with open(file_name, encoding='utf8') as f:
    #     for line in f:
        for line in text.split('\n'):
            # TODO: должно помочь от подвисания интерфейса
            app.processEvents()

            line = line.rstrip()

            if line:
                # TODO: рефакторинг
                # Определим игровую платформу: ПК, консоли и т.п.
                if (line[0] not in [' ', '-', '@'] and line[0] not in [' ', '-', '@']) and line.endswith(':'):
                    set_count_children_nodes(platform)

                    # Имя платформы без двоеточия на конце
                    platform = line[0: len(line) - 1]
                    platform_item = QTreeWidgetItem([platform])
                    self.tree_games.addTopLevelItem(platform_item)

                    delete_empty_nodes()

                    finished_game_items = QTreeWidgetItem([FINISHED_GAME_TITLE])
                    not_finished_game_items = QTreeWidgetItem([NOT_FINISHED_GAME_TITLE])
                    finished_watched_items = QTreeWidgetItem([FINISHED_WATCHED_TITLE])
                    not_finished_watched_items = QTreeWidgetItem([NOT_FINISHED_WATCHED_TITLE])

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
                            strange_game_platform_item = QTreeWidgetItem([platform])
                            strange_platform_games_dict[platform] = strange_game_platform_item
                            strange_games.addChild(strange_game_platform_item)
                        else:
                            strange_game_platform_item = strange_platform_games_dict[platform]

                        logger.warning('!!! Обнаружен неизвестный атрибут !!!: ' + unknown_attributes + ', игра: '
                                       + line + ', платформа: ' + platform)
                        game_item = QTreeWidgetItem([line])
                        strange_game_platform_item.addChild(game_item)
                        continue

                    # TODO: рефакторинг
                    is_finished_watched = attributes == '@ ' or attributes == ' @'
                    is_not_finished_watched = attributes == '@-' or attributes == '-@'

                    is_finished_game = attributes == '  '
                    is_not_finished_game = attributes == '- ' or attributes == ' -'

                    # TODO: rem
                    game_name = line[2:]
                    # platforms_game_dict[platform] = game_name

                    game_item = QTreeWidgetItem([game_name])
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
                            strange_game_platform_item = QTreeWidgetItem([platform])
                            strange_platform_games_dict[platform] = strange_game_platform_item
                            strange_games.addChild(strange_game_platform_item)
                        else:
                            strange_game_platform_item = strange_platform_games_dict[platform]

                        game_item.setText(0, line + ' / ' + platform)
                        strange_game_platform_item.addChild(game_item)

        set_count_children_nodes(platform)
        delete_empty_nodes()

        # Добавляем узел неопределенных игр
        if strange_games.childCount() > 0:
            self.tree_games.addTopLevelItem(strange_games)
        else:
            strange_games = None

        # print(platforms_game_dict)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.show()
    mw.refresh_by_url()

    sys.exit(app.exec_())
