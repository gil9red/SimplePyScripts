#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import base64
from os.path import split as path_split
import traceback
import sys

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *

except:
    try:
        from PyQt4.QtGui import *
        from PyQt4.QtCore import *
    except:
        from PySide.QtGui import *
        from PySide.QtCore import *


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, 'Error', text)
    quit()


sys.excepthook = log_uncaught_exceptions


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(path_split(__file__)[1])

        self.button_direct = QPushButton()

        # # TODO: добавить больше кодировок, и лучше не вручную
        # cb_encoding = QComboBox()
        # cb_encoding.addItem('UTF-8')
        # cb_encoding.addItem('CP1251')
        # cb_encoding.addItem('UTF-16LE')
        # cb_encoding.addItem('UTF-16BE')
        # cb_encoding.setCurrentIndex(0)
        # cb_encoding.setFixedWidth(100)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_direct)
        # button_layout.addWidget(cb_encoding)

        layout = QVBoxLayout()
        layout.addLayout(button_layout)

        self.text_edit_input = QPlainTextEdit()

        self.text_edit_output = QPlainTextEdit()
        self.text_edit_output.setReadOnly(True)

        # True -- кодирование текста, False -- раскодирование
        self.direct_encode_text = False

        self.label_error = QLabel()
        self.label_error.setStyleSheet("QLabel { color : red; }")
        self.label_error.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label_error.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.button_detail_error = QPushButton('...')
        self.button_detail_error.setFixedSize(20, 20)
        self.button_detail_error.setToolTip('Detail error')
        self.button_detail_error.clicked.connect(self.show_detail_error_massage)

        self.last_error_message = None
        self.last_detail_error_message = None

        # Первый вызов, чтобы у кнопки появился текст
        self.change_convert_direct()

        self.button_direct.clicked.connect(self.change_convert_direct)
        self.text_edit_input.textChanged.connect(self.input_text_changed)
        # cb_encoding.currentIndexChanged.connect(input_text_changed)

        splitter = QSplitter()
        splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        splitter.addWidget(self.text_edit_input)
        splitter.addWidget(self.text_edit_output)

        layout.addWidget(splitter)

        layout_error = QHBoxLayout()
        layout_error.addWidget(self.label_error)
        layout_error.addWidget(self.button_detail_error)

        layout.addLayout(layout_error)

        self.setLayout(layout)

    def show_detail_error_massage(self):
        message = self.last_error_message + '\n\n' + self.last_detail_error_message

        mb = QErrorMessage()
        mb.setWindowTitle('Error')
        # Сообщение ошибки содержит отступы, символы-переходы на следующую строку,
        # которые поломаются при вставке через QErrorMessage.showMessage, и нет возможности
        # выбрать тип текста, то делаем такой хак.
        mb.findChild(QTextEdit).setPlainText(message)

        mb.exec_()

    def input_text_changed(self):
        self.label_error.clear()
        self.button_detail_error.hide()

        self.last_error_message = None
        self.last_detail_error_message = None

        try:
            # codec_name = cb_encoding.currentText()
            # text = text_edit_input.toPlainText().encode()
            # text = base64.b64encode(text) if direct_encode_text else base64.b64decode(text)
            # text_edit_output.setPlainText(
            #     text.decode() if direct_encode_text else text.decode('utf-8').encode(codec_name).decode()
            # )

            # text = text_edit_input.toPlainText().encode() if not direct_encode_text else \
            #     text_edit_input.toPlainText().encode(codec_name)
            # print(text)
            # text = base64.b64encode(text) if direct_encode_text else base64.b64decode(text)
            # text_edit_output.setPlainText(text.decode() if not direct_encode_text else text.decode(codec_name))

            text = self.text_edit_input.toPlainText().encode()
            text = base64.b64encode(text) if self.direct_encode_text else base64.b64decode(text)
            self.text_edit_output.setPlainText(text.decode())

        except Exception as e:
            # Выводим ошибку в консоль
            traceback.print_exc()

            # Сохраняем в переменную
            tb = traceback.format_exc()

            self.last_error_message = str(e)
            self.last_detail_error_message = str(tb)
            self.button_detail_error.show()

            self.label_error.setText('Error: ' + self.last_error_message)

    def change_convert_direct(self):
        self.direct_encode_text = not self.direct_encode_text

        self.button_direct.setText('text -> base64' if self.direct_encode_text else 'base64 -> text')

        self.input_text_changed()


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.resize(650, 500)
    mw.show()

    sys.exit(app.exec_())
