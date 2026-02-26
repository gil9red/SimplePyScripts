#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import ctypes
from ctypes.wintypes import DWORD, ULONG
from ctypes import windll, c_bool, c_int, POINTER, Structure

from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt


class AccentPolicy(Structure):
    _fields_ = [
        ("AccentState", DWORD),
        ("AccentFlags", DWORD),
        ("GradientColor", DWORD),
        ("AnimationId", DWORD),
    ]


# SOURCE: http://undoc.airesoft.co.uk/user32.dll/GetWindowCompositionAttribute.php
class WINCOMPATTRDATA(Structure):
    _fields_ = [
        ("Attribute", DWORD),
        ("Data", POINTER(AccentPolicy)),
        ("SizeOfData", ULONG),
    ]


# SOURCE: http://undoc.airesoft.co.uk/user32.dll/SetWindowCompositionAttribute.php
# BOOL WINAPI SetWindowCompositionAttribute (
#     HWND hwnd,
#     WINCOMPATTRDATA* pAttrData
# )
SetWindowCompositionAttribute = windll.user32.SetWindowCompositionAttribute
SetWindowCompositionAttribute.restype = c_bool
SetWindowCompositionAttribute.argtypes = [c_int, POINTER(WINCOMPATTRDATA)]


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)

        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)

        # SOURCE: http://howtucode.com/c-pinvoke-user32dll-getwindowcompositionattribute-13192.html
        accent_policy = AccentPolicy()
        accent_policy.AccentState = 3  # ACCENT_ENABLE_BLURBEHIND;

        win_comp_attr_data = WINCOMPATTRDATA()
        win_comp_attr_data.Attribute = 19  # WCA_ACCENT_POLICY
        win_comp_attr_data.SizeOfData = ctypes.sizeof(accent_policy)
        win_comp_attr_data.Data = ctypes.pointer(accent_policy)

        hwnd = c_int(self.winId())
        ok = SetWindowCompositionAttribute(hwnd, ctypes.pointer(win_comp_attr_data))
        print(ok)

        print(ctypes.get_last_error())

        self._old_pos = None
        self.frame_color = Qt.darkCyan

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(QPushButton("Закрыть окно", clicked=self.close))

        self.setLayout(layout)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self._old_pos = event.pos()

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self._old_pos = None

    def mouseMoveEvent(self, event) -> None:
        if not self._old_pos:
            return

        delta = event.pos() - self._old_pos
        self.move(self.pos() + delta)


if __name__ == "__main__":
    app = QApplication([])

    w = Widget()
    w.resize(400, 300)
    w.show()

    app.exec()
