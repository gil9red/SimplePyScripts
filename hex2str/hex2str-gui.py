#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: обоюдное выделеление текста в полях ввода
# TODO: конвертирование в обе стороны


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

    last_select_start, last_select_end = None, None

#     def selection_changed():
#         """Обновляем выделение у текстовых редакторов"""
#
#         # text_edit_input -- hex значения
#         # text_edit_output -- строковые значения, каждые два hex представляютсяодним символом
#
#
# #         cursor.selectionEnd()
# #
# # QTextCursor::MoveAnchor	0	Moves the anchor to the same position as the cursor itself.
# # QTextCursor::KeepAnchor	1	Keeps the anchor where it is.
# #
# # void QTextCursor::setPosition ( int pos, MoveMode m = MoveAnchor )
# # bool QTextCursor::movePosition ( MoveOperation operation, MoveMode mode = MoveAnchor, int n = 1 )
#
#         global last_select_start, last_select_end
#
#         if text_edit_input.hasFocus():
#             cursor = QTextCursor(text_edit_input.textCursor())
#             start, end = cursor.selectionStart(), cursor.selectionEnd()
#             selection_len = len(cursor.selectedText())
#
#             if selection_len == 0:
#                 last_select_start, last_select_end = start, end
#                 return
#
#             if last_select_start == start and last_select_end == end:
#                 return
#
#             print('start={} end={} len={}'.format(start, end, selection_len)
#                   + ' | ' + 'last_start={} last_end={}'.format(last_select_start, last_select_end))
#
#             if last_select_end is not None and end >= last_select_end:
#             # if True:
#                 n = selection_len
#                 # # if n % 2 == 1 and n > 1:
#                 # #     n -= 1
#                 # # elif n == 1:
#                 # #     n = 2
#
#                 cursor.setPosition(start, QTextCursor.MoveAnchor)
#
#                 # if n % 2 == 1 and start < last_select_start and last_select_start is not None:
#                 #     n += 1
#                 #     cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, n)
#
#                 # cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, n)
#
#                 # if n % 2 == 1 and start < last_select_start and last_select_start is not None:
#                 #     n += 1
#                 if n % 2 == 1:
#                     n += 1
#
#                 # print('r', selection_len, n)
#
#                 cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, n)
#                 text_edit_input.setTextCursor(cursor)
#
#             # elif last_select_start is not None and last_select_start < start:
#             elif last_select_start is not None and start < last_select_start:
#                 n = selection_len
#                 # # if n % 2 == 1 and n > 1:
#                 # #     n -= 1
#                 # # elif n == 1:
#                 # #     n = 2
#
#                 cursor.setPosition(end, QTextCursor.MoveAnchor)
#
#                 # if n % 2 == 1 and start < last_select_start and last_select_start is not None:
#                 #     n += 1
#                 #     cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, n)
#
#                 # cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, n)
#
#                 # # if n % 2 == 1 and start < last_select_start and last_select_start is not None:
#                 # #     n += 1
#                 # if n % 2 == 1:
#                 #     n -= 1
#
#                 cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, n)
#                 text_edit_input.setTextCursor(cursor)
#
#             last_select_start, last_select_end = start, end
#
#         # if text_edit_input.hasFocus():
#         #     cursor = QTextCursor(text_edit_input.textCursor())
#         #
#         #     start, end = cursor.selectionStart(), cursor.selectionEnd()
#         #
#         #     cursor.setPosition(start // 2, QTextCursor.MoveAnchor)
#         #     cursor.movePosition(QTextCursor.Right if end > start else QTextCursor.Left, QTextCursor.KeepAnchor, (max(end, start) - min(end, start)) / 2)
#         #
#         #     print(start, (max(end, start) - min(end, start)), (max(end, start) - min(end, start)) / 2)
#         #
#         #     text_edit_output.setTextCursor(cursor)
#         #
#         # elif text_edit_output.hasFocus():
#         #     cursor = QTextCursor(text_edit_output.textCursor())
#         #     text_edit_input.setTextCursor(cursor)
#
#     text_edit_input.selectionChanged.connect(selection_changed)
#     text_edit_output.selectionChanged.connect(selection_changed)

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

    text_edit_input.setPlainText('504F53542068747470733A')

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
