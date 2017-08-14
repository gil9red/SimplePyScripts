#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


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


# TODO: обоюдное выделеление текста в полях ввода: выделяешь в hex строке выделяется его аналог в тексте и наоборот
# TODO: конвертирование в обе стороны


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('hex2str')

        self.text_edit_input = QPlainTextEdit()
        self.text_edit_input.textChanged.connect(self.input_text_changed)

        self.text_edit_output = QPlainTextEdit()

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

        layout_left_side = QVBoxLayout()
        layout_left_side.setContentsMargins(0, 0, 0, 0)
        layout_left_side.addWidget(QLabel('Input:'))
        layout_left_side.addWidget(self.text_edit_input)
        left_side = QWidget()
        left_side.setLayout(layout_left_side)

        layout_right_side = QVBoxLayout()
        layout_right_side.setContentsMargins(0, 0, 0, 0)
        layout_right_side.addWidget(QLabel('Output:'))
        layout_right_side.addWidget(self.text_edit_output)
        right_side = QWidget()
        right_side.setLayout(layout_right_side)

        splitter = QSplitter()
        splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        splitter.addWidget(left_side)
        splitter.addWidget(right_side)

        layout_error = QHBoxLayout()
        layout_error.addWidget(self.label_error)
        layout_error.addWidget(self.button_detail_error)

        layout = QVBoxLayout()
        layout.addWidget(splitter)
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
            text = self.text_edit_input.toPlainText()

            from hex2str import hex2str
            text = hex2str(text)

            self.text_edit_output.setPlainText(text)

        except Exception as e:
            # Выводим ошибку в консоль
            import traceback
            traceback.print_exc()

            # Сохраняем в переменную
            tb = traceback.format_exc()

            self.last_error_message = str(e)
            self.last_detail_error_message = str(tb)
            self.button_detail_error.show()

            self.label_error.setText('Error: ' + self.last_error_message)


if __name__ == '__main__':
    app = QApplication([])

    mw = Widget()
    mw.resize(650, 500)
    mw.text_edit_input.setPlainText('504F53542068747470733A')
    mw.show()

    sys.exit(app.exec_())
