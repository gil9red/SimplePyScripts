#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    import base64
    from os.path import split as path_split
    import traceback
    import sys

    from PySide.QtGui import *
    from PySide.QtCore import *

    app = QApplication(sys.argv)

    mainWidget = QWidget()
    mainWidget.setWindowTitle(path_split(__file__)[1])

    layout = QVBoxLayout()

    button_direct = QPushButton()

    # # TODO: добавить больше кодировок, и лучше не вручную
    # cb_encoding = QComboBox()
    # cb_encoding.addItem('UTF-8')
    # cb_encoding.addItem('CP1251')
    # cb_encoding.addItem('UTF-16LE')
    # cb_encoding.addItem('UTF-16BE')
    # cb_encoding.setCurrentIndex(0)
    # cb_encoding.setFixedWidth(100)

    button_layout = QHBoxLayout()
    button_layout.addWidget(button_direct)
    # button_layout.addWidget(cb_encoding)

    layout.addLayout(button_layout)

    text_edit_input = QPlainTextEdit()

    text_edit_output = QPlainTextEdit()
    text_edit_output.setReadOnly(True)

    # True -- кодирование текста, False -- раскодирование
    direct_encode_text = False

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

            text = text_edit_input.toPlainText().encode()
            text = base64.b64encode(text) if direct_encode_text else base64.b64decode(text)
            text_edit_output.setPlainText(text.decode())
        except Exception as e:
            # Выводим ошибку в консоль
            traceback.print_exc()

            # Сохраняем в переменную
            tb = traceback.format_exc()

            last_error_message = str(e)
            last_detail_error_message = str(tb)
            button_detail_error.show()

            label_error.setText('Error: ' + last_error_message)

    def change_convert_direct():
        global direct_encode_text
        direct_encode_text = not direct_encode_text

        button_direct.setText('text -> base64' if direct_encode_text else 'base64 -> text')

        input_text_changed()

    # Первый вызов, чтобы у кнопки появился текст
    change_convert_direct()

    button_direct.clicked.connect(change_convert_direct)
    text_edit_input.textChanged.connect(input_text_changed)
    # cb_encoding.currentIndexChanged.connect(input_text_changed)

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
