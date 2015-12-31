#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys

from urllib.request import urlopen, urlretrieve
from urllib.parse import urljoin

from lxml import etree
from io import StringIO

from PySide.QtGui import *


from common import get_logger


logger = get_logger('played_games')


DEFAULT_URL = 'https://gist.github.com/gil9red/2f80a34fb601cd685353'


def add_tree_widget_item_platform(platform):
    return QTreeWidgetItem(['{} ({}):'.format(platform.name, platform.count_games)])


def add_tree_widget_item_category(category):
    return QTreeWidgetItem(['{} ({}):'.format(ENUM_CATEGORY_TITLE_DICT[category.kind], category.count)])


def add_tree_widget_item_game(game):
    return QTreeWidgetItem([game.name])


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
    app.parser.processEvents()


TEST_USING_FILE_GAMES = True


WINDOW_TITLE = 'Played Games'
TREE_HEADER = 'Games'
OTHER_GAME_TITLE = 'Неопределенные игры'


from played_games_parser import Parser

ENUM_CATEGORY_TITLE_DICT = {
    Parser.CategoryEnum.FINISHED_GAME: 'Пройденные',
    Parser.CategoryEnum.NOT_FINISHED_GAME: 'Не закончено прохождение',
    Parser.CategoryEnum.FINISHED_WATCHED: 'Просмотренные',
    Parser.CategoryEnum.NOT_FINISHED_WATCHED: 'Не закончен просмотр',
}


# Последовательность добавления категорий в узел платформы
SEQ_ADDED_CATEGORIES = [Parser.CategoryEnum.FINISHED_GAME,
                        Parser.CategoryEnum.NOT_FINISHED_GAME,
                        Parser.CategoryEnum.FINISHED_WATCHED,
                        Parser.CategoryEnum.NOT_FINISHED_WATCHED]


# TODO: добавить кнопку сортировки
# TODO: сделать модель дерева
# TODO: кнопку показа статистики: игры, платформы
# TODO: избавить от подвисания программы во время загрузки файла и его парсинга
# TODO: показывать прогресс загрузки из сети файла (хотя бы в процентах)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(WINDOW_TITLE)

        self.tree_games = QTreeWidget()

        self.line_edit_url = QLineEdit(DEFAULT_URL)
        self.button_refresh_by_url = QPushButton('&Refresh')
        self.button_refresh_by_url.clicked.connect(self.refresh_by_url)

        # # TODO: немного грязный хак, используемый для настройки парсировки, без задания gui
        # self.magic_window = QWidget()
        # self.magic_window.setWindowTitle('Magic!')
        #
        # self.button_magic_window = QPushButton(self.magic_window.windowTitle())
        # self.button_magic_window.clicked.connect(lambda x=None:
        #                                          self.magic_window.move(self.x() + self.width() + 20, self.y()) or
        #                                          self.magic_window.show())
        # self.text_edit_magic_window = QPlainTextEdit()
        # self.button_run_magic_window = QPushButton('Run Magic')
        # layout = QVBoxLayout()
        # layout.addWidget(self.text_edit_magic_window)
        # layout.addWidget(self.button_run_magic_window)
        # self.magic_window.setLayout(layout)
        # self.button_run_magic_window.clicked.connect(lambda x=None:
        #                                              print(self.text_edit_magic_window.toPlainText().encode()) or
        #                                              eval(self.text_edit_magic_window.toPlainText()))

        layout = QHBoxLayout()
        layout.addWidget(self.line_edit_url)
        layout.addWidget(self.button_refresh_by_url)
        # layout.addWidget(self.button_magic_window)

        self.line_edit_filter = QLineEdit()
        self.line_edit_filter.setToolTip('Wildcard Filter')
        self.line_edit_filter.textEdited.connect(self.load_tree)

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

        self.parser = Parser()
        self.parse_content = None

        self.update_header_tree_and_window_title()

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

                # Ищем первый файл с кнопкой Raw
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

        self.parse_content = content_file
        self.load_tree()

    def load_tree(self):
        logger.debug('Start build tree.')

        self.parser.parse(self.parse_content,
                          self.line_edit_filter.text(),
                          parse_game_name_on_sequence=True,
                          sort_game=False
                          )
        self.tree_games.clear()

        for k, v in self.parser.sorted_platforms:
            platform_item = add_tree_widget_item_platform(v)
            self.tree_games.addTopLevelItem(platform_item)

            for kind in SEQ_ADDED_CATEGORIES:
                if kind not in v.categories:
                    continue

                category = v.categories[kind]
                category_item = add_tree_widget_item_category(category)
                platform_item.addChild(category_item)

                for game in category:
                    game_item = add_tree_widget_item_game(game)
                    category_item.addChild(game_item)

        if self.parser.other.count_games > 0:
            other_item = QTreeWidgetItem(['{} ({}):'.format(OTHER_GAME_TITLE, self.parser.other.count_games)])
            self.tree_games.addTopLevelItem(other_item)

            for k, v in self.parser.other.platforms.items():
                platform_item = add_tree_widget_item_platform(v)
                other_item.addChild(platform_item)

                for category in v.categories.values():
                    for game in category:
                        game_item = add_tree_widget_item_game(game)
                        platform_item.addChild(game_item)

        self.tree_games.expandAll()
        self.update_header_tree_and_window_title()

    def update_header_tree_and_window_title(self):
        # Указываем в заголовке общее количество игр и при фильтр, количество игр, оставшихся после фильтрации
        self.tree_games.setHeaderLabel('{} ({})'.format(TREE_HEADER, self.parser.count_games))

        # Обновление заголовка окна
        self.setWindowTitle('{}. Platforms: {}. Games: {}'.format(WINDOW_TITLE,
                                                                  self.parser.count_platforms,
                                                                  self.parser.count_games))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.show()
    mw.refresh_by_url()

    sys.exit(app.exec_())
