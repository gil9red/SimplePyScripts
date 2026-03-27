#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QPushButton,
    QCheckBox,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen

from grid_clicker import click_all_on_screen


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
        self.do_click: bool = True
        self.need_run_clicker: bool = False

        self.checkbox_do_click = QCheckBox(
            "Do Click?", checked=self.do_click, clicked=self.on_checkbox_do_click
        )

        self.button_run = QPushButton("Run click", clicked=self.on_run_clicked)
        self.button_close = QPushButton("Close", clicked=self.close)

        self.control_widget = QFrame(self)
        self.control_widget.setCursor(Qt.ArrowCursor)
        self.control_widget.setStyleSheet(
            """
            QFrame {
                background-color: rgba(60, 60, 60, 200);
                border-radius: 10px;
            }
            QCheckBox {
                color: white;
            }
        """
        )
        self.control_widget.hide()
        control_layout = QVBoxLayout(self.control_widget)
        control_layout.addWidget(self.checkbox_do_click)
        control_layout.addWidget(self.button_run)
        control_layout.addWidget(self.button_close)

    def on_run_clicked(self):
        self.need_run_clicker = True
        self.close()

    def on_checkbox_do_click(self):
        self.do_click = self.checkbox_do_click.isChecked()

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

            local_begin = self.mapFromGlobal(self.begin_global)
            self.control_widget.move(local_begin)
            self.control_widget.show()

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.is_selecting = False

            self.selected_rect = QRect(self.begin_global, self.end_global).normalized()

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

        if selector.need_run_clicker:
            click_all_on_screen(
                do_click=selector.do_click,
                sleep_time_before_starting_secs=1,
                coords=(x1, y1, x2, y2),
            )

    else:
        print("Выбор отменен.")

    # NOTE: Не нужен для QDialog.exec
    # sys.exit(app.exec())
