#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


import time
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
    sys.exit(1)


import sys
sys.excepthook = log_uncaught_exceptions


class MainWindow(QWidget):
    ESCAPE_RULES = [
        ('"', '"', r'\"', True),
        ("'", "'", r"\'", True),
        (r'\n', "\n", r'\n', True),
        (r'\t', "\t", r'\t', True),
        (r'\b', "\b", r'\b', True),
        (r'\f', "\f", r'\f', False),
        ('\\', "\\", '\\\\', False),
    ]
    TITLE = 'EscapeString'

    def __init__(self):
        super().__init__()

        self.setWindowTitle(self.TITLE)

        self.escape_char_by_checkbox = {}
        self.char_by_escape = {}

        button_layout = QHBoxLayout()
        for title, char, escape, checked in self.ESCAPE_RULES:
            checkbox = QCheckBox(title)
            checkbox.setChecked(checked)
            checkbox.clicked.connect(self.input_text_changed)

            font = checkbox.font()
            font.setBold(True)
            font.setPointSize(font.pointSize() + 2)
            checkbox.setFont(font)

            button_layout.addWidget(checkbox)
            self.escape_char_by_checkbox[char] = checkbox
            self.char_by_escape[char] = escape

        button_layout.addStretch()

        self.cb_string_literal = QCheckBox('String literal')
        self.cb_string_literal.setChecked(True)
        self.cb_string_literal.clicked.connect(self.input_text_changed)

        button_layout.addWidget(self.cb_string_literal)

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
        self.button_detail_error.hide()

        self.last_error_message = None
        self.last_detail_error_message = None

        self.text_edit_input.textChanged.connect(self.input_text_changed)

        self.label_input_number = QLabel()
        self.label_output_number = QLabel()

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
        if not self.last_error_message or not self.last_detail_error_message:
            return

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
            t = time.perf_counter()

            out_text = self.text_edit_input.toPlainText()

            new_out_text = []

            for char in out_text:
                # Если char нет в словаре экранирования или флаг экранирования для char выключен
                if char not in self.escape_char_by_checkbox or not self.escape_char_by_checkbox[char].isChecked():
                    new_out_text.append(char)
                    continue

                new_out_text.append(self.char_by_escape[char])

            out_text = ''.join(new_out_text)

            if self.cb_string_literal.isChecked():
                out_text = f'"{out_text}";'

            self.text_edit_output.setPlainText(out_text)

            self.setWindowTitle(
                f'{self.TITLE} (number of characters: '
                f'{len(self.text_edit_input.toPlainText())} -> '
                f'{len(self.text_edit_output.toPlainText())})'
            )
            print('Escape for {:.6f} secs'.format(time.perf_counter() - t))

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
