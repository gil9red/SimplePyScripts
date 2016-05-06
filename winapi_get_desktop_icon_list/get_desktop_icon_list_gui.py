#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_desktop_resolution():
    """
    Функция возвращает разрешение экрана.

    """

    from ctypes.wintypes import RECT
    from win32con import MONITOR_DEFAULTTONEAREST

    import ctypes
    MonitorFromWindow = ctypes.windll.user32.MonitorFromWindow
    GetMonitorInfo = ctypes.windll.user32.GetMonitorInfoW

    from winapi_GetDesktopListViewHandle import GetDesktopListViewHandle

    class MONITORINFO(ctypes.Structure):
        _fields_ = [
            ('cbSize', ctypes.c_int),
            ('rcMonitor', RECT),
            ('rcWork', RECT),
            ('dwFlags', ctypes.c_int),
        ]

    hwnd = GetDesktopListViewHandle()
    monitor = MonitorFromWindow(hwnd, MONITOR_DEFAULTTONEAREST)
    info = MONITORINFO()
    info.cbSize = ctypes.sizeof(MONITORINFO)

    GetMonitorInfo(monitor, ctypes.byref(info))
    width = info.rcMonitor.right - info.rcMonitor.left
    height = info.rcMonitor.bottom - info.rcMonitor.top
    return width, height


from get_desktop_icon_list import get_desktop_icons_list

if __name__ == '__main__':
    import sys

    from PySide.QtGui import *
    from PySide.QtCore import *

    app = QApplication(sys.argv)

    scene = QGraphicsScene()

    width_desktop, height_desktop = get_desktop_resolution()

    scene_rect = QRectF(0, 0, width_desktop, height_desktop)
    scene.addRect(scene_rect)
    scene.setSceneRect(scene_rect)

    for i, name, pos, rect in get_desktop_icons_list():
        x, y, w, h = pos.x, pos.y, rect.right - rect.left, rect.bottom - rect.top
        scene.addRect(x, y, w, h)

    view = QGraphicsView()
    view.setWindowTitle('winapi_get_desktop_icon_list')
    view.setScene(scene)

    n = 3
    view.scale(1.0 / n, 1.0 / n)
    view.show()

    app.exec_()
