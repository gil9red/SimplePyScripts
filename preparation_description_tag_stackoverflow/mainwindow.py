#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import pickle
import shutil
import os
import traceback

from PySide.QtGui import *
from PySide.QtCore import *

from mainwindow_ui import Ui_MainWindow
from common import *


logger = get_logger('mainwindow')
DIR = 'tags'
DIR = 'tags3'


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

        self.ui.ref_guide.textChanged.connect(self.ref_guide_text_changed)
        self.ui.description.textChanged.connect(self.description_text_changed)

        # # TODO: заменить модель комбобокса нашим списком
        self.tags_dict = dict()
        self.modified_tags = set()

        # TODO: комбобокс заменить списком / таблицей

        self.update_states()

    def update_states(self):
        self.ui.action_save_tag.setEnabled(False)

        index = self.ui.tag_list.currentIndex()
        if index < 0:
            return

        tag_id = self.ui.tag_list.itemData(index)
        self.ui.action_save_tag.setEnabled(tag_id in self.modified_tags)

    def fill_tag_list(self):
        self.ui.tag_list.clear()
        self.tags_dict.clear()

        tag_file_list = [DIR + '/' + tag for tag in os.listdir(DIR) if tag.endswith('.tag')]
        for file_name in tag_file_list:
            with open(file_name, 'rb') as f:
                # Пример: {'ref_guide': '', 'id': '1', 'description': '', 'name': ['python']}
                data = pickle.load(f)
                data['hash'] = self.hash_tag(data)

                self.tags_dict[data['id']] = data

        self.ui.tag_list.blockSignals(True)

        print('Total tags:', len(self.tags_dict))

        for id_tag, tag in sorted(self.tags_dict.items(), key=lambda x: int(x[0])):
            name = '#{}: {}'.format(id_tag, ', '.join(tag['name']))
            self.ui.tag_list.addItem(name, id_tag)

            QApplication.processEvents()

        self.ui.tag_list.blockSignals(False)

        if self.ui.tag_list.count():
            self.fill_tag_info(0)

        self.update_states()

    def hash_tag(self, tag):
        text = tag['ref_guide'] + tag['description']

        import hashlib
        md5 = hashlib.md5()
        md5.update(text.encode())
        return md5.hexdigest()

    def check_modified_tag(self, tag_id):
        tag = self.tags_dict[tag_id]

        new_hash = self.hash_tag(tag)

        if tag['hash'] == new_hash:
            if tag_id in self.modified_tags:
                self.modified_tags.remove(tag_id)
        else:
            self.modified_tags.add(tag_id)

    def ref_guide_text_changed(self):
        index = self.ui.tag_list.currentIndex()
        if index < 0:
            return

        tag_id = self.ui.tag_list.itemData(index)
        tag = self.tags_dict[tag_id]
        tag['ref_guide'] = self.ui.ref_guide.toPlainText()

        self.check_modified_tag(tag_id)
        self.update_states()

    def description_text_changed(self):
        index = self.ui.tag_list.currentIndex()
        if index < 0:
            return

        tag_id = self.ui.tag_list.itemData(index)
        tag = self.tags_dict[tag_id]
        tag['description'] = self.ui.description.toPlainText()

        self.check_modified_tag(tag_id)
        self.update_states()

    def fill_tag_info(self, index):
        if index < 0:
            return

        tag_id = self.ui.tag_list.itemData(index)
        tag = self.tags_dict[tag_id]
        print('fill_tag_info', tag, hex(id(tag)))

        url = 'http://ru.stackoverflow.com/tags/{}/info'.format(tag['name'][0])
        url = '<a href="{0}">{0}</a>'.format(url)
        self.ui.url.setText(url)

        self.ui.ref_guide.blockSignals(True)
        self.ui.description.blockSignals(True)

        self.ui.ref_guide.setPlainText(tag['ref_guide'])
        self.ui.description.setPlainText(tag['description'])

        self.ui.ref_guide.blockSignals(False)
        self.ui.description.blockSignals(False)

        self.update_states()

    def save_tag(self):
        index = self.ui.tag_list.currentIndex()
        if index < 0:
            return

        tag_id = self.ui.tag_list.itemData(index)
        tag = self.tags_dict[tag_id]

        file_name = DIR + '/{}.tag'.format(tag['id'])
        file_name_backup = file_name + '.backup'

        # Перед переписыванием файла, делаем его копию
        shutil.copyfile(file_name, file_name_backup)

        try:
            with open(file_name, mode='wb') as f:
                # Обновляем хеш
                tag['hash'] = self.hash_tag(tag)

                # Флаг, говорящий, что данный тег был изменен пользователем
                tag['user_changed'] = True

                self.modified_tags.remove(tag_id)

                pickle.dump(tag, f)

        except Exception as e:
            logger.error('{}.\n\n{}'.format(e, traceback.format_exc()))
            logger.debug('Restore {} from {}.'.format(file_name, file_name_backup))

            # Произошла ошибка. Восстанавливаем файл из бекапа
            os.remove(file_name)
            os.rename(file_name_backup, file_name)
        else:
            logger.debug('Update {} was successful, removed the backup: {}.'.format(file_name, file_name_backup))

            # Переписывание прошло хорошо, удаляем файл бекапа
            if os.path.exists(file_name_backup):
                os.remove(file_name_backup)

        self.update_states()

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
