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

    # Уменьшение размеров / положений, чтобы не создавалось больше окно
    # TODO: испльзовать штатные средства сцены для уменьшения масштаба
    n = 4

    app = QApplication(sys.argv)

    scene = QGraphicsScene()

    width_desktop, height_desktop = get_desktop_resolution()
    width_desktop //= n
    height_desktop //= n
    scene.addRect(0, 0, width_desktop, height_desktop)
    scene.setSceneRect(0, 0, width_desktop, height_desktop)

    for i, name, pos, rect in get_desktop_icons_list():
        x, y, w, h = pos.x, pos.y, rect.right - rect.left, rect.bottom - rect.top
        x //= n
        y //= n
        w //= n
        h //= n
        scene.addRect(x, y, w, h)

    view = QGraphicsView()
    view.setWindowTitle('winapi_get_desktop_icon_list')
    view.setScene(scene)

    view.show()

    app.exec_()

    # icons_list = get_desktop_icons_list()
    #
    # # # Сортировка по положению на экране
    # # for i, name, pos in sorted(icons_list, key=lambda x: (x[2].x, x[2].y)):
    # #
    # # # # Сортировка по индексу
    # # for i, name, pos, rect in sorted(icons_list, key=lambda x: x[0]):
    # #     print('{0: >3}. "{1}": {2.x}x{2.y}, {3.left}x{3.top} {3.right}x{3.bottom}'.format(i + 1, name, pos, rect))
    # # # Сортировка по индексу
    # for i, name, pos, rect in sorted(icons_list, key=lambda x: x[0]):
    #     print('{0: >3}. "{1}": {2.x}x{2.y}, {3}x{4}'.format(i + 1,
    #                                                         name,
    #                                                         pos,
    #                                                         rect.right - rect.left,
    #                                                         rect.bottom - rect.top,
    #                                                         ))
