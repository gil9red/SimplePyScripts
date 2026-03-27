#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen


class AreaSelectorDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setCursor(Qt.CrossCursor)

        self.full_geometry = QApplication.desktop().geometry()
        self.setGeometry(self.full_geometry)

        self.begin_global = QPoint()  # Глобальная точка начала
        self.end_global = QPoint()  # Глобальная точка конца
        self.is_selecting = False

        self.selected_rect: QRect | None = None

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.begin_global = event.globalPos()
            self.end_global = self.begin_global
            self.is_selecting = True
            self.update()

    def mouseMoveEvent(self, event) -> None:
        if self.is_selecting:
            self.end_global = event.globalPos()
            self.update()

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.is_selecting = False

            self.selected_rect = QRect(self.begin_global, self.end_global).normalized()
            self.close()

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Escape:
            self.close()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)

        painter.fillRect(self.rect(), QColor(0, 0, 0, 80))

        if self.is_selecting:
            local_begin = self.mapFromGlobal(self.begin_global)
            local_end = self.mapFromGlobal(self.end_global)
            rect = QRect(local_begin, local_end).normalized()

            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.fillRect(rect, Qt.transparent)
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.drawRect(rect)


if __name__ == "__main__":
    # Поддержка высокого DPI (важно для правильных координат на 4K мониторах)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)

    selector = AreaSelectorDialog()
    selector.exec()

    selected_rect = selector.selected_rect
    if selector.selected_rect:
        _, _, w, h = selected_rect.getRect()

        # Извлекаем границы
        x1 = selected_rect.left()
        x2 = selected_rect.right()
        y1 = selected_rect.top()
        y2 = selected_rect.bottom()

        print("--- Координаты ---")
        print(f"x1={x1}, y1={y1}, x2={x2}, y2={y2}")
        print(f"Tuple: ({x1}, {y1}, {x2}, {y2})")
        print(f"Args: --x1={x1} --y1={y1} --x2={x2} --y2={y2}")
        print(f"Размер: {w}x{h}")
        print("------------------------------")
    else:
        print("Выбор отменен.")

    # NOTE: Не нужен для QDialog.exec
    # sys.exit(app.exec())
