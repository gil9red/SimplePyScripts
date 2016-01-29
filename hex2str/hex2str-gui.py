#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    from os.path import split as path_split
    import traceback
    import sys

    from PySide.QtGui import *
    from PySide.QtCore import *

    import hex2str

    app = QApplication(sys.argv)

    mainWidget = QWidget()
    mainWidget.setWindowTitle(path_split(__file__)[1])

    layout = QVBoxLayout()

    text_edit_input = QPlainTextEdit()
    text_edit_output = QPlainTextEdit()

    label_error = QLabel()
    label_error.setStyleSheet("QLabel { color : red; }")
    label_error.setTextInteractionFlags(Qt.TextSelectableByMouse)
    label_error.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    button_detail_error = QPushButton('...')
    button_detail_error.setFixedSize(20, 20)
    button_detail_error.setToolTip('Detail error')
    last_error_message = None
    last_detail_error_message = None

    def show_detail_error_massage():
        message = last_error_message + '\n\n' + last_detail_error_message

        mb = QErrorMessage()
        mb.setWindowTitle('Error')
        # Сообщение ошибки содержит отступы, символы-переходы на следующую строку,
        # которые поломаются при вставке через QErrorMessage.showMessage, и нет возможности
        # выбрать тип текста, то делаем такой хак.
        mb.findChild(QTextEdit).setPlainText(message)

        mb.exec_()

    button_detail_error.clicked.connect(show_detail_error_massage)

    def input_text_changed():
        label_error.clear()
        button_detail_error.hide()

        global last_error_message, last_detail_error_message
        last_error_message = None
        last_detail_error_message = None

        try:
            text = text_edit_input.toPlainText()
            text = hex2str.do(text)
            text_edit_output.setPlainText(text)
        except Exception as e:
            # Выводим ошибку в консоль
            traceback.print_exc()

            # Сохраняем в переменную
            tb = traceback.format_exc()

            last_error_message = str(e)
            last_detail_error_message = str(tb)
            button_detail_error.show()

            label_error.setText('Error: ' + last_error_message)

    text_edit_input.textChanged.connect(input_text_changed)

    splitter = QSplitter()
    splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    splitter.addWidget(text_edit_input)
    splitter.addWidget(text_edit_output)

    layout.addWidget(splitter)

    layout_error = QHBoxLayout()
    layout_error.addWidget(label_error)
    layout_error.addWidget(button_detail_error)

    layout.addLayout(layout_error)

    mainWidget.setLayout(layout)

    mainWidget.resize(650, 500)
    mainWidget.show()

    sys.exit(app.exec_())
