#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install psutil
import psutil

# pip install pyvda
import pyvda

# pip install win32gui
import win32gui

# pip install pywin32
import win32process


NEED_WINDOW_DESKTOP_NUMBER = 2


def get_hwnd_for_pid(pid: int):
    def callback(hwnd: int, hwnds: list):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
                return True
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds[0] if hwnds else -1


for proc in psutil.process_iter():
    if not proc.is_running() or proc.name() != 'ConEmu.exe':
        continue

    hwnd = get_hwnd_for_pid(proc.pid)

    # If the window is already on the desired desktop
    if hwnd == -1 or pyvda.GetWindowDesktopNumber(hwnd) == NEED_WINDOW_DESKTOP_NUMBER:
        continue

    print(f'Moved window (pid={proc.pid}) to window desktop #{NEED_WINDOW_DESKTOP_NUMBER}')
    pyvda.MoveWindowToDesktopNumber(hwnd, NEED_WINDOW_DESKTOP_NUMBER)
