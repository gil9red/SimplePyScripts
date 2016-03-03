#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# https://gist.github.com/gil9red/6f7648c9dfc446083d46


"""Используется вместе с SimplePyScripts\Grab\empty_tags_stackoverflow.py
Скрипт empty_tags_stackoverflow.py собирает найденные пустые теги и выводит их в консоль.

В итоге получилось множество такого вида. Второй и третий параметр -- отсутствие руководства и отсутствие описания
тега:

tag_list = {('history', True, True, 'http://ru.stackoverflow.com/tags/history/info'),
            ('suse', True, True, 'http://ru.stackoverflow.com/tags/suse/info'),
            ('qbasic', True, True, 'http://ru.stackoverflow.com/tags/qbasic/info'),
            ...


И это множество тегов было сохранено в виде файлов. Для каждого тега был создан отдельный файл вида:

<tag>
    <name></name>
    <url></url>
    <ref_guide></ref_guide>
    <description></description>
</tag>


"""


import sys
from PySide.QtGui import QApplication
from mainwindow import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.read_settings()
    mw.show()

    mw.fill_tag_list()

    sys.exit(app.exec_())
