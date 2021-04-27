#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import base64
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
    text += ''.join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, 'Error', text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


# from encodings.aliases import aliases
# print(aliases)
# OR:
STANDART_ENCODINGS = [
    "ascii",
    "big5",
    "big5hkscs",
    "cp037",
    "cp424",
    "cp437",
    "cp500",
    "cp720",
    "cp737",
    "cp775",
    "cp850",
    "cp852",
    "cp855",
    "cp856",
    "cp857",
    "cp858",
    "cp860",
    "cp861",
    "cp862",
    "cp863",
    "cp864",
    "cp865",
    "cp866",
    "cp869",
    "cp874",
    "cp875",
    "cp932",
    "cp949",
    "cp950",
    "cp1006",
    "cp1026",
    "cp1140",
    "cp1250",
    "cp1251",
    "cp1252",
    "cp1253",
    "cp1254",
    "cp1255",
    "cp1256",
    "cp1257",
    "cp1258",
    "euc_jp",
    "euc_jis_2004",
    "euc_jisx0213",
    "euc_kr",
    "gb2312",
    "gbk",
    "gb18030",
    "hz",
    "iso2022_jp",
    "iso2022_jp_1",
    "iso2022_jp_2",
    "iso2022_jp_2004",
    "iso2022_jp_3",
    "iso2022_jp_ext",
    "iso2022_kr",
    "latin_1",
    "iso8859_2",
    "iso8859_3",
    "iso8859_4",
    "iso8859_5",
    "iso8859_6",
    "iso8859_7",
    "iso8859_8",
    "iso8859_9",
    "iso8859_10",
    "iso8859_13",
    "iso8859_14",
    "iso8859_15",
    "iso8859_16",
    "johab",
    "koi8_r",
    "koi8_u",
    "mac_cyrillic",
    "mac_greek",
    "mac_iceland",
    "mac_latin2",
    "mac_roman",
    "mac_turkish",
    "ptcp154",
    "shift_jis",
    "shift_jis_2004",
    "shift_jisx0213",
    "utf_32",
    "utf_32_be",
    "utf_32_le",
    "utf_16",
    "utf_16_be",
    "utf_16_le",
    "utf_7",
    "utf_8",
    "utf_8_sig"
]


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        from os.path import split as path_split
        self.setWindowTitle(path_split(__file__)[1])

        self.button_direct = QPushButton()
        self.button_direct.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.cb_encoding = QComboBox()
        self.cb_encoding.addItems(STANDART_ENCODINGS)
        self.cb_encoding.setFixedWidth(100)

        index = self.cb_encoding.findText('utf_8')
        self.cb_encoding.setCurrentIndex(index)

        self.cb_raw = QCheckBox('raw')

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_direct)
        button_layout.addWidget(self.cb_encoding)
        button_layout.addWidget(self.cb_raw)

        layout = QVBoxLayout()
        layout.addLayout(button_layout)

        self.text_edit_input = QPlainTextEdit()

        self.text_edit_output = QPlainTextEdit()
        self.text_edit_output.setReadOnly(True)

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

        # True -- кодирование текста, False -- раскодирование
        self.direct_encode_text = True

        # Первый вызов, чтобы у кнопки появился текст (заодно это сменит режим кодирования)
        self.change_convert_direct()

        self.button_direct.clicked.connect(self.change_convert_direct)
        self.text_edit_input.textChanged.connect(self.input_text_changed)
        self.cb_encoding.currentIndexChanged.connect(self.input_text_changed)
        self.cb_raw.clicked.connect(self.input_text_changed)

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
            codec_name = self.cb_encoding.currentText()
            in_text = self.text_edit_input.toPlainText().encode(encoding=codec_name)

            if self.direct_encode_text:
                text = base64.b64encode(in_text)
            else:
                text = base64.b64decode(in_text)

            # Для 'raw' не делаем декодирование, а показываем представление объекта как строку
            if self.cb_raw.isChecked():
                text = repr(text)
            else:
                # Параметр errors='replace' нужен для того, чтобы при декодировании в строку проблемные символы
                # заменялись символами-заменителями (�)
                text = text.decode(encoding=codec_name, errors='replace')

            self.text_edit_output.setPlainText(text)

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
