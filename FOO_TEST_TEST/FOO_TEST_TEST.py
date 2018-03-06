#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


import traceback

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


import sys
sys.excepthook = log_uncaught_exceptions


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        from os.path import split as path_split
        self.setWindowTitle(path_split(__file__)[1])

        self.escape_rules = [
            ('"', '"', r'\"', True),
            ("'", "'", r"\'", True),
            (r'\n', "\n", r'\n', True),
        ]
        self.checkbox_by_escape = {}

        button_layout = QHBoxLayout()
        for title, char, escape, checked in self.escape_rules:
            checkbox = QCheckBox(title)
            checkbox.setChecked(checked)
            checkbox.clicked.connect(self.input_text_changed)

            font = checkbox.font()
            font.setBold(True)
            font.setPointSize(font.pointSize() + 2)
            checkbox.setFont(font)

            button_layout.addWidget(checkbox)
            self.checkbox_by_escape[checkbox] = (char, escape)

        button_layout.addStretch()

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

        self.text_edit_input.textChanged.connect(self.input_text_changed)

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
            out_text = self.text_edit_input.toPlainText()

            for checkbox, (char, escape) in self.checkbox_by_escape.items():
                if not checkbox.isChecked():
                    continue

                out_text = out_text.replace(char, escape)

            # out_text = in_text.replace('"', r'\"').replace("'", r"\'").replace("\n", r"\n").replace("\t", r"\t")

            self.text_edit_output.setPlainText(out_text)

        except Exception as e:
            # Выводим ошибку в консоль
            traceback.print_exc()

            # Сохраняем в переменную
            tb = traceback.format_exc()

            self.last_error_message = str(e)
            self.last_detail_error_message = str(tb)
            self.button_detail_error.show()

            self.label_error.setText('Error: ' + self.last_error_message)


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.resize(650, 500)
    mw.show()

    sys.exit(app.exec_())
