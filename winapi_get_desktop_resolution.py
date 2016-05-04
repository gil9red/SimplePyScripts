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


if __name__ == '__main__':
    w, h = get_desktop_resolution()
    print(w, h, sep='x')
