#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from io import StringIO
import json
import time
import sys

from urllib.request import urlopen, urlretrieve
from urllib.parse import urljoin

from lxml import etree

from PySide.QtGui import *
from PySide.QtCore import *


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
    app.processEvents()


WINDOW_TITLE = 'Played Games'
TREE_HEADER = 'Games'
OTHER_GAME_TITLE = 'Неопределенные игры'

CONFIG_FILE = 'config'


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


# TODO: сделать модель дерева
# TODO: кнопку показа статистики: игры, платформы
# TODO: избавить от подвисания программы во время загрузки файла и его парсинга
# TODO: показывать прогресс загрузки из сети файла (хотя бы в процентах)
# TODO: обновлять дерево при смене настроек


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(WINDOW_TITLE)

        self.tree_games = QTreeWidget()

        self.line_edit_url = QLineEdit(DEFAULT_URL)
        self.button_refresh_by_url = QPushButton('&Refresh')
        self.button_refresh_by_url.clicked.connect(self.refresh_by_url)

        self.dock_widget_settings = QDockWidget('Settings')
        self.dock_widget_settings.setObjectName(self.dock_widget_settings.windowTitle())
        layout = QFormLayout()
        self.TEST_USING_FILE_GAMES = QCheckBox()
        self.PARSE_GAME_NAME_ON_SEQUENCE = QCheckBox()
        self.SORT_GAME = QCheckBox()
        self.SORT_REVERSE = QCheckBox()
        label_SORT_REVERSE = QLabel('SORT_REVERSE')
        self.SORT_GAME.toggled.connect(self.SORT_REVERSE.setVisible)
        self.SORT_GAME.toggled.connect(label_SORT_REVERSE.setVisible)
        self.DONT_SHOW_NUMBER_1_ON_GAME = QCheckBox()

        self.TEST_USING_FILE_GAMES.setChecked(True)
        self.PARSE_GAME_NAME_ON_SEQUENCE.setChecked(True)
        self.SORT_GAME.setChecked(False)
        self.SORT_REVERSE.setChecked(False)
        self.DONT_SHOW_NUMBER_1_ON_GAME.setChecked(False)

        self.SORT_REVERSE.setVisible(self.SORT_GAME.isChecked())
        label_SORT_REVERSE.setVisible(self.SORT_GAME.isChecked())

        layout.addRow("TEST_USING_FILE_GAMES", self.TEST_USING_FILE_GAMES)
        layout.addRow("PARSE_GAME_NAME_ON_SEQUENCE", self.PARSE_GAME_NAME_ON_SEQUENCE)
        layout.addRow("SORT_GAME", self.SORT_GAME)
        layout.addRow(label_SORT_REVERSE, self.SORT_REVERSE)
        layout.addRow("DONT_SHOW_NUMBER_1_ON_GAME", self.DONT_SHOW_NUMBER_1_ON_GAME)
        widget = QWidget()
        widget.setLayout(layout)

        self.dock_widget_settings.setWidget(widget)
        self.dock_widget_settings.hide()
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget_settings)

        general_tool_bar = self.addToolBar('General')
        general_tool_bar.setObjectName(general_tool_bar.windowTitle())
        general_tool_bar.addAction(self.dock_widget_settings.toggleViewAction())

        # tool_bar_gist_url = self.addToolBar('Gist Url')
        # layout = QHBoxLayout()
        # layout.addWidget(self.line_edit_url)
        # layout.addWidget(self.button_refresh_by_url)
        # widget = QWidget()
        # widget.setLayout(layout)
        # tool_bar_gist_url.addWidget(widget)
        #
        # tool_bar_filter = self.addToolBar('Filter')
        # layout = QHBoxLayout()
        # self.line_edit_filter = QLineEdit()
        # self.line_edit_filter.setToolTip('Wildcard Filter')
        # self.line_edit_filter.textEdited.connect(self.load_tree)
        #
        # layout.addWidget(QLabel('Filter:'))
        # layout.addWidget(self.line_edit_filter)
        # widget = QWidget()
        # widget.setLayout(layout)
        # tool_bar_filter.addWidget(widget)

        layout = QHBoxLayout()
        layout.addWidget(self.line_edit_url)
        layout.addWidget(self.button_refresh_by_url)

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

        self.read_settings()

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

        logger.debug('TEST_USING_FILE_GAMES = {}.'.format(self.TEST_USING_FILE_GAMES.isChecked()))

        if self.TEST_USING_FILE_GAMES.isChecked():
            # TODO: для тестирования интерфейса
            test_file_name = 'gistfile1.txt'

            logger.debug('Open and read {} start.'.format(test_file_name))
            with open(test_file_name, 'r', encoding='utf8') as f:
                content_file = f.read()
            logger.debug('Finish open and read. Content file length = {}.'.format(len(content_file)))
        else:
            # PROGRESS_BAR.show()
            # PROGRESS_BAR.setValue(-1)

            url = self.line_edit_url.text()

            # Теперь нужно получить url файла с последней ревизией
            logger.debug('Get url file last revision start.')
            t = time.clock()

            with urlopen(url) as f:
                context = f.read().decode()

                parser = etree.HTMLParser()
                tree = etree.parse(StringIO(context), parser)

                # Ищем первый файл с кнопкой Raw
                rel_url = tree.xpath('//*[@class="btn btn-sm "]/@href')[0]
                logger.debug('Relative url = {}.'.format(rel_url))

                url = urljoin(url, str(rel_url))
                logger.debug('Full url = {}.'.format(url))

            logger.debug('Get url file last revision finish. Elapsed time: {:.3f} ms.'.format(time.clock() - t))

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
                          self.PARSE_GAME_NAME_ON_SEQUENCE.isChecked(),
                          self.SORT_GAME.isChecked(),
                          self.SORT_REVERSE.isChecked(),
                          self.DONT_SHOW_NUMBER_1_ON_GAME.isChecked(),
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

    def read_settings(self):
        logger.debug('Start read_settings. CONFIG_FILE={}.'.format(CONFIG_FILE))

        try:
            with open(CONFIG_FILE, encoding='utf-8') as f:
                settings = json.load(f)

                self.TEST_USING_FILE_GAMES.setChecked(settings['TEST_USING_FILE_GAMES'])
                self.PARSE_GAME_NAME_ON_SEQUENCE.setChecked(settings['PARSE_GAME_NAME_ON_SEQUENCE'])
                self.SORT_GAME.setChecked(settings['SORT_GAME'])
                self.SORT_REVERSE.setChecked(settings['SORT_REVERSE'])
                self.DONT_SHOW_NUMBER_1_ON_GAME.setChecked(settings['DONT_SHOW_NUMBER_1_ON_GAME'])

                state = QByteArray.fromBase64(settings['MainWindow_State'])
                self.restoreState(state)

                geometry = QByteArray.fromBase64(settings['MainWindow_Geometry'])
                self.restoreGeometry(geometry)

        except Exception as e:
            logger.warning(e)
            logger.debug("Заполняю значения по умолчанию.")

            self.TEST_USING_FILE_GAMES.setChecked(True)
            self.PARSE_GAME_NAME_ON_SEQUENCE.setChecked(True)
            self.SORT_GAME.setChecked(False)
            self.SORT_REVERSE.setChecked(False)
            self.DONT_SHOW_NUMBER_1_ON_GAME.setChecked(False)

        logger.debug('Finish read_settings.')

    def write_settings(self):
        logger.debug('Start write_settings. CONFIG_FILE={}.'.format(CONFIG_FILE))
        logger.debug('Build dict.')

        settings = {
            'TEST_USING_FILE_GAMES': self.TEST_USING_FILE_GAMES.isChecked(),
            'PARSE_GAME_NAME_ON_SEQUENCE': self.PARSE_GAME_NAME_ON_SEQUENCE.isChecked(),
            'SORT_GAME': self.SORT_GAME.isChecked(),
            'SORT_REVERSE': self.SORT_REVERSE.isChecked(),
            'DONT_SHOW_NUMBER_1_ON_GAME': self.DONT_SHOW_NUMBER_1_ON_GAME.isChecked(),

            'MainWindow_State': str(self.saveState().toBase64()),
            'MainWindow_Geometry': str(self.saveGeometry().toBase64()),
        }

        logger.debug('Write config.')

        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            str_json_obj = json.dumps(settings, sort_keys=True, indent=4)
            f.write(str_json_obj)

        logger.debug('Finish write_settings.')

    def closeEvent(self, event):
        self.write_settings()
        quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.show()
    mw.refresh_by_url()

    sys.exit(app.exec_())
