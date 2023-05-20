#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import traceback
import sys

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *

except:
    try:
        from PyQt4.QtGui import *
        from PyQt4.QtCore import *

    except:
        from PySide.QtGui import *
        from PySide.QtCore import *

# Выбор функции конвертации в зависимости от значения радио-кнопки
from hex2str import hex2str, str2hex


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("hex2str")

        self.radio_button_hex2str = QRadioButton("hex2str")
        self.radio_button_hex2str.setChecked(True)

        self.radio_button_str2hex = QRadioButton("str2hex")

        self.text_edit_input = QPlainTextEdit()
        self.text_edit_input.textChanged.connect(self._convert)
        self.text_edit_input.selectionChanged.connect(self._on_input_selection_changed)

        self.text_edit_output = QPlainTextEdit()
        self.text_edit_output.selectionChanged.connect(
            self._on_output_selection_changed
        )

        # Изменение цвета выделения текста, чтобы при отсутствии фокуса был такой же цвет как при его наличии
        palette = self.text_edit_input.palette()
        palette.setColor(
            QPalette.Inactive,
            QPalette.Highlight,
            palette.color(QPalette.Active, QPalette.Highlight),
        )
        palette.setColor(
            QPalette.Inactive,
            QPalette.HighlightedText,
            palette.color(QPalette.Active, QPalette.HighlightedText),
        )
        self.text_edit_input.setPalette(palette)
        self.text_edit_output.setPalette(palette)

        self.label_error = QLabel()
        self.label_error.setStyleSheet("QLabel { color : red; }")
        self.label_error.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label_error.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.button_detail_error = QPushButton("...")
        self.button_detail_error.setFixedSize(20, 20)
        self.button_detail_error.setToolTip("Detail error")
        self.button_detail_error.clicked.connect(self.show_detail_error_massage)

        self.last_error_message = None
        self.last_detail_error_message = None

        layout_left_side = QVBoxLayout()
        layout_left_side.setContentsMargins(0, 0, 0, 0)
        layout_left_side.addWidget(QLabel("Input:"))
        layout_left_side.addWidget(self.text_edit_input)
        left_side = QWidget()
        left_side.setLayout(layout_left_side)

        layout_right_side = QVBoxLayout()
        layout_right_side.setContentsMargins(0, 0, 0, 0)
        layout_right_side.addWidget(QLabel("Output:"))
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

        self._button_group = QButtonGroup()
        self._button_group.addButton(self.radio_button_hex2str)
        self._button_group.addButton(self.radio_button_str2hex)
        self._button_group.buttonClicked.connect(self._convert)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.radio_button_hex2str)
        button_layout.addWidget(self.radio_button_str2hex)

        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(splitter)
        layout.addLayout(layout_error)

        self.setLayout(layout)

    def _on_input_selection_changed(self):
        try:
            # Нехорошо будет если второй будет вызывать сигналы, например о выделении текста
            self.text_edit_output.blockSignals(True)

            cursor = self.text_edit_input.textCursor()
            if not cursor.hasSelection():
                cursor_output = self.text_edit_output.textCursor()
                cursor_output.clearSelection()
                self.text_edit_output.setTextCursor(cursor_output)
                return

            start = cursor.selectionStart()
            end = cursor.selectionEnd()

            # Hex символов в 2 раза больше чем их символьных представлений
            is_hex2str = self.radio_button_hex2str.isChecked()
            if is_hex2str:
                new_start, new_end = start // 2, end // 2
            else:
                new_start, new_end = start * 2, end * 2

            cursor_output = self.text_edit_output.textCursor()
            cursor_output.setPosition(new_start, QTextCursor.MoveAnchor)
            cursor_output.setPosition(new_end, QTextCursor.KeepAnchor)

            self.text_edit_output.setTextCursor(cursor_output)

        finally:
            self.text_edit_output.blockSignals(False)

    def _on_output_selection_changed(self):
        try:
            # Нехорошо будет если второй будет вызывать сигналы, например о выделении текста
            self.text_edit_input.blockSignals(True)

            cursor = self.text_edit_output.textCursor()
            if not cursor.hasSelection():
                cursor_output = self.text_edit_input.textCursor()
                cursor_output.clearSelection()
                self.text_edit_input.setTextCursor(cursor_output)
                return

            start = cursor.selectionStart()
            end = cursor.selectionEnd()

            # Hex символов в 2 раза больше чем их символьных представлений
            is_hex2str = self.radio_button_hex2str.isChecked()
            if not is_hex2str:
                new_start, new_end = start // 2, end // 2
            else:
                new_start, new_end = start * 2, end * 2

            cursor_output = self.text_edit_input.textCursor()
            cursor_output.setPosition(new_start, QTextCursor.MoveAnchor)
            cursor_output.setPosition(new_end, QTextCursor.KeepAnchor)

            self.text_edit_input.setTextCursor(cursor_output)

        finally:
            self.text_edit_input.blockSignals(False)

    def show_detail_error_massage(self):
        message = self.last_error_message + "\n\n" + self.last_detail_error_message

        mb = QErrorMessage()
        mb.setWindowTitle("Error")
        # Сообщение ошибки содержит отступы, символы-переходы на следующую строку,
        # которые поломаются при вставке через QErrorMessage.showMessage, и нет возможности
        # выбрать тип текста, то делаем такой хак.
        mb.findChild(QTextEdit).setPlainText(message)

        mb.exec_()

    def _convert(self):
        self.label_error.clear()
        self.button_detail_error.hide()

        self.last_error_message = None
        self.last_detail_error_message = None

        try:
            func = hex2str if self.radio_button_hex2str.isChecked() else str2hex

            text = self.text_edit_input.toPlainText()
            text = func(text)

            self.text_edit_output.setPlainText(text)

        except Exception as e:
            # Выводим ошибку в консоль
            traceback.print_exc()

            # Сохраняем в переменную
            tb = traceback.format_exc()

            self.last_error_message = str(e)
            self.last_detail_error_message = str(tb)
            self.button_detail_error.show()

            self.label_error.setText("Error: " + self.last_error_message)


if __name__ == "__main__":
    app = QApplication([])

    mw = Widget()
    mw.resize(650, 500)
    mw.text_edit_input.setPlainText("504F53542068747470733A")
    mw.show()

    sys.exit(app.exec_())
