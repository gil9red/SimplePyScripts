#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/00b9e4ec67e3413ffefa436a98381a75b99af6d3/qt__pyqt__pyside__pyqode/pyqt__frameless_window_with_part_transparent_body.py


import traceback
import sys
from pathlib import Path

from flask import Flask, jsonify

from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QPoint, QThread, pyqtSignal, QTimer, QByteArray, QBuffer
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap, QCursor, QMouseEvent, QKeyEvent, QPaintEvent

from config import PORT, PATH_DEFAULT_MOUSE


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f'{ex_cls.__name__}: {ex}:\n'
    text += ''.join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, 'Error', text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class CommandServerThread(QThread):
    about_command = pyqtSignal(str)

    def __init__(self, parent=None, port=PORT):
        super().__init__(parent)

        self.port = port
        self.pixmap_data = bytes()
        self.app = Flask(__name__)

        @self.app.route("/command/<command>", methods=['POST'])
        def command(command: str):
            print(command)
            self.about_command.emit(command)

            if command == 'SCREENSHOT' and self.pixmap_data:
                return self.pixmap_data

            return jsonify({'status': True})

    def set_pixmap(self, pixmap_data: bytes):
        self.pixmap_data = pixmap_data

    def run(self):
        self.app.run(port=self.port)


class MainWindow(QWidget):
    def __init__(self, port=PORT, mouse_permeability=True):
        super().__init__()

        self.setWindowTitle(Path(__file__).name)

        self.setWindowFlags(
            self.windowFlags()
            | Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.DEFAULT_MOUSE_PIXMAP = QPixmap(PATH_DEFAULT_MOUSE).scaledToWidth(16)

        self._old_pos = None
        self.frame_color = Qt.red
        self.frame_size = 15
        self.mouse_permeability = mouse_permeability

        self.button_hide = QPushButton("Hide")
        self.button_hide.clicked.connect(self.hide)

        self.button_close = QPushButton("Close")
        self.button_close.clicked.connect(self.close)

        self.layout_buttons = QHBoxLayout()
        self.layout_buttons.addWidget(self.button_hide)
        self.layout_buttons.addWidget(self.button_close)

        main_layout = QVBoxLayout(self)
        main_layout.addStretch()
        main_layout.addLayout(self.layout_buttons)

        self.thread_command = CommandServerThread(self, port=port)
        self.thread_command.about_command.connect(self.process_command)
        self.thread_command.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self._on_tick)
        self.timer.start(30)

    def _on_stats_query(self):
        self.thread_screenshot.set_stats(self.geometry(), self.isVisible())

    def _on_tick(self):
        if self.isHidden():
            return

        geometry = self.geometry()
        x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()

        # Корректировка области скриншота, чтобы не захватывать рамку и кнопки
        correct_frame_size = self.frame_size // 2 + 1
        x += correct_frame_size
        y += correct_frame_size
        h = self.layout_buttons.geometry().y() - correct_frame_size
        w -= correct_frame_size * 2

        pixmap = QApplication.instance().primaryScreen().grabWindow(
            QApplication.desktop().winId(),
            x, y, w, h
        )

        cursor_pos = QCursor.pos()
        local_pos = self.mapFromGlobal(cursor_pos)

        if self.rect().contains(local_pos):
            painter = QPainter()
            painter.begin(pixmap)
            painter.drawPixmap(local_pos, self.DEFAULT_MOUSE_PIXMAP)
            painter.end()

        data = QByteArray()
        buffer = QBuffer(data)
        buffer.open(QBuffer.WriteOnly)
        pixmap.save(buffer, "JPG")

        self.thread_command.set_pixmap(bytes(data))

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._old_pos = event.pos()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._old_pos = None

    def mouseMoveEvent(self, event: QMouseEvent):
        if not self._old_pos:
            return

        delta = event.pos() - self._old_pos
        self.move(self.pos() + delta)

    def move_left(self):
        self.move(self.pos() + QPoint(-10, 0))

    def move_right(self):
        self.move(self.pos() + QPoint(10, 0))

    def move_up(self):
        self.move(self.pos() + QPoint(0, -10))

    def move_down(self):
        self.move(self.pos() + QPoint(0, 10))

    def process_command(self, command: str):
        command = command.upper()

        if command == 'LEFT':
            self.move_left()
        elif command == 'RIGHT':
            self.move_right()
        elif command == 'UP':
            self.move_up()
        elif command == 'DOWN':
            self.move_down()
        elif command == 'HIDE':
            self.hide()
        elif command == 'SHOW':
            self.show()
        elif command == 'MOVE_TO_CURSOR':
            rect = self.geometry()
            rect.moveCenter(QCursor.pos())
            self.setGeometry(rect)

    def keyReleaseEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Left:
            self.move_left()
        elif event.key() == Qt.Key_Right:
            self.move_right()
        elif event.key() == Qt.Key_Up:
            self.move_up()
        elif event.key() == Qt.Key_Down:
            self.move_down()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)

        painter.setBrush(QColor(0, 0, 0, 0 if self.mouse_permeability else 1))
        painter.setPen(QPen(self.frame_color, self.frame_size))

        painter.drawRect(self.rect())


def main(port=PORT, is_visible=True, width=800, height=600, mouse_permeability=True):
    app = QApplication([])

    w = MainWindow(port, mouse_permeability)
    w.resize(width, height)

    if is_visible:
        w.show()

    app.exec()


if __name__ == '__main__':
    main(mouse_permeability=False)
