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
    QFormLayout,
    QSpinBox,
)
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen, QMouseEvent, QKeyEvent, QPaintEvent

from grid_clicker import click_all_on_screen


# TODO: Поддержка сохранения и восстановления области
class AreaSelectorDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setCursor(Qt.CursorShape.CrossCursor)

        full_geometry: QRect = QApplication.desktop().geometry()
        self.setGeometry(full_geometry)

        self._begin_global: QPoint = QPoint()  # Глобальная точка начала
        self._end_global: QPoint = QPoint()  # Глобальная точка конца
        self._is_selecting: bool = False

        self.selected_rect: QRect | None = None
        self.need_run_clicker: bool = False

        self.checkbox_do_click = QCheckBox(checked=True)
        self.spin_box_step = QSpinBox(value=50)
        self.button_run = QPushButton("Run click", clicked=self.on_run_clicked)
        self.button_close = QPushButton("Close", clicked=self.close)

        self.control_widget = QFrame(self)
        self.control_widget.setCursor(Qt.ArrowCursor)
        self.control_widget.setStyleSheet("""
            QFrame {
                background-color: rgba(60, 60, 60, 200);
                border-radius: 10px;
            }
            QCheckBox,
            QLabel {
                color: white;
            }
        """)
        self.control_widget.hide()
        control_layout = QFormLayout(self.control_widget)
        control_layout.addRow("Do &Click?:", self.checkbox_do_click)
        control_layout.addRow("&Step:", self.spin_box_step)
        control_layout.addRow(self.button_run)
        control_layout.addRow(self.button_close)

    @property
    def step(self) -> int:
        return self.spin_box_step.value()

    @property
    def do_click(self) -> bool:
        return self.checkbox_do_click.isChecked()

    def on_run_clicked(self) -> None:
        self.need_run_clicker = True
        self.close()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self._begin_global = event.globalPos()
            self._end_global = self._begin_global
            self._is_selecting = True
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._is_selecting:
            self._end_global = event.globalPos()
            self.update()

            local_begin = self.mapFromGlobal(self._begin_global)
            self.control_widget.move(local_begin)
            self.control_widget.show()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self._is_selecting = False
            self.selected_rect = QRect(
                self._begin_global, self._end_global
            ).normalized()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Escape:
            self.close()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))

        if self._is_selecting:
            local_begin = self.mapFromGlobal(self._begin_global)
            local_end = self.mapFromGlobal(self._end_global)
            rect = QRect(local_begin, local_end).normalized()

            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.fillRect(rect, QColor(255, 255, 255, 1))
            painter.drawRect(rect)


if __name__ == "__main__":
    # Поддержка высокого DPI (важно для правильных координат на 4K мониторах)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)

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
                step=selector.step,
                sleep_time_before_starting_secs=1,
                coords=(x1, y1, x2, y2),
            )

    else:
        print("Выбор отменен.")

    # NOTE: Не нужен для QDialog.exec
    # sys.exit(app.exec())
