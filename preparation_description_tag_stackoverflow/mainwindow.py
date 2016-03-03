#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import shutil
import os
import traceback

import glob
from lxml import etree

from PySide.QtGui import *
from PySide.QtCore import *

from mainwindow_ui import Ui_MainWindow


CONFIG_FILE = 'config'


class MainWindow(QMainWindow, QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle('Preparation description tag stackoverflow')

        # Все действия к прикрепляемым окнам поместим в меню
        for dock in self.findChildren(QDockWidget):
            self.ui.menuDockWindow.addAction(dock.toggleViewAction())

        # Все действия к toolbar'ам окнам поместим в меню
        for tool in self.findChildren(QToolBar):
            self.ui.menuTools.addAction(tool.toggleViewAction())

        self.ui.tag_list.currentIndexChanged.connect(self.fill_tag_info)

        self.ui.action_save_tag.triggered.connect(self.save_tag)

        # TODO: remove
        self.ui.name.hide()
        self.ui.label_name.hide()

        self.ui.action_reread_tag.setVisible(False)

    def fill_tag_list(self):
        self.ui.tag_list.clear()

        for tag in glob.glob('tags/*.tag'):
            tag_el = etree.parse(tag).getroot()
            name = tag_el.xpath('./name')[0].text

            self.ui.tag_list.addItem(name, etree.parse(tag))

            QApplication.processEvents()

        if self.ui.tag_list.count():
            self.fill_tag_info(0)

    def fill_tag_info(self, index):
        if index < 0:
            return

        tag_el = self.ui.tag_list.itemData(index).getroot()

        self.ui.name.setText(tag_el.xpath('./name')[0].text)

        url = '<a href="{0}">{0}</a>'.format(tag_el.xpath('./url')[0].text)
        self.ui.url.setText(url)
        self.ui.url.setToolTip(self.ui.url.text())

        self.ui.ref_guide.setPlainText(tag_el.xpath('./ref_guide')[0].text)
        self.ui.description.setPlainText(tag_el.xpath('./description')[0].text)

    def save_tag(self):
        index = self.ui.tag_list.currentIndex()
        if index < 0:
            return

        tag_el = self.ui.tag_list.itemData(index).getroot()
        tag_el.xpath('./ref_guide')[0].text = self.ui.ref_guide.toPlainText()
        tag_el.xpath('./description')[0].text = self.ui.description.toPlainText()

        file_name = 'tags/{}.tag'.format(tag_el.xpath('./name')[0].text)
        file_name_backup = file_name + '.backup'

        # Перед переписыванием файла, делаем его копию
        shutil.copyfile(file_name, file_name_backup)

        try:
            with open(file_name, mode='wb') as f:
                f.write(etree.tostring(tag_el, pretty_print=True))

        except Exception as e:
            print('ERROR: {}.\n\n{}'.format(e, traceback.format_exc()))
            print('Restore {} from {}.'.format(file_name, file_name_backup))

            # Произошла ошибка. Восстанавливаем файл из бекапа
            os.remove(file_name)
            os.rename(file_name_backup, file_name)
        else:
            print('Update {} was successful, removed the backup: {}.'.format(file_name, file_name_backup))

            # Переписывание прошло хорошо, удаляем файл бекапа
            if os.path.exists(file_name_backup):
                os.remove(file_name_backup)

    def read_settings(self):
        # TODO: при сложных настройках, лучше перейти на json или yaml
        config = QSettings(CONFIG_FILE, QSettings.IniFormat)
        self.restoreState(config.value('MainWindow_State'))
        self.restoreGeometry(config.value('MainWindow_Geometry'))
        self.ui.splitter.restoreState(config.value('Splitter_State'))

    def write_settings(self):
        config = QSettings(CONFIG_FILE, QSettings.IniFormat)
        config.setValue('MainWindow_State', self.saveState())
        config.setValue('MainWindow_Geometry', self.saveGeometry())
        config.setValue('Splitter_State', self.ui.splitter.saveState())

    def closeEvent(self, event):
        self.write_settings()
        quit()
