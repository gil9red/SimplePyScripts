#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import struct
import ctypes
from ctypes.wintypes import POINT, RECT

import commctrl
from commctrl import (
    LVIF_TEXT,
    LVM_GETITEMTEXT,
    LVM_GETITEMPOSITION,
    LVIR_BOUNDS,
    LVM_GETITEMRECT,
)

from win32con import PROCESS_ALL_ACCESS, GW_CHILD, MEM_RESERVE, MEM_COMMIT, PAGE_READWRITE, MEM_RELEASE


def GetDesktopListViewHandle():
    """
    Функция возвращает указатель на ListView рабочего стола.

    Оригинал:
    function GetDesktopListViewHandle: THandle;
        var
            S: string;
        begin
            Result := FindWindow('ProgMan', nil);
            Result := GetWindow(Result, GW_CHILD);
            Result := GetWindow(Result, GW_CHILD);
            SetLength(S, 40);
            GetClassName(Result, PChar(S), 39);
            if PChar(S) <> 'SysListView32' then
                Result := 0;
        end;

    """

    FindWindow = ctypes.windll.user32.FindWindowW
    GetWindow = ctypes.windll.user32.GetWindow

    def GetClassName(hwnd):
        buff = ctypes.create_unicode_buffer(100)
        ctypes.windll.user32.GetClassNameW(hwnd, buff, 99)
        return buff.value

    # Ищем окно с классом "Progman" ("Program Manager")
    hwnd = FindWindow("Progman", None)
    hwnd = GetWindow(hwnd, GW_CHILD)  # SHELLDLL_DefView
    hwnd = GetWindow(hwnd, GW_CHILD)  # SysListView32

    if GetClassName(hwnd) != "SysListView32":
        return 0

    return hwnd


def ListView_GetItemCount(hwnd):
    """

    Функция возвращает количество элементов указанного ListView.

    Оригинал:
    define ListView_GetItemCount(hwnd) (int)SNDMSG((hwnd),LVM_GETITEMCOUNT,(WPARAM)0,(LPARAM)0)

    """

    SendMessage = ctypes.windll.user32.SendMessageW

    return SendMessage(hwnd, commctrl.LVM_GETITEMCOUNT, 0, 0)


class LVITEMW(ctypes.Structure):
    _fields_ = [
        ("mask", ctypes.c_uint32),
        ("iItem", ctypes.c_int32),
        ("iSubItem", ctypes.c_int32),
        ("state", ctypes.c_uint32),
        ("stateMask", ctypes.c_uint32),
        ("pszText", ctypes.c_uint64),
        ("cchTextMax", ctypes.c_int32),
        ("iImage", ctypes.c_int32),
        ("lParam", ctypes.c_uint64),  # On 32 bit should be c_long
        ("iIndent", ctypes.c_int32),
        ("iGroupId", ctypes.c_int32),
        ("cColumns", ctypes.c_uint32),
        ("puColumns", ctypes.c_uint64),
        ("piColFmt", ctypes.c_int64),
        ("iGroup", ctypes.c_int32),
    ]


def get_desktop_process_handle(hwnd=None):
    GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
    OpenProcess = ctypes.windll.kernel32.OpenProcess

    if hwnd is None:
        hwnd = GetDesktopListViewHandle()

    pid = ctypes.create_string_buffer(4)
    p_pid = ctypes.addressof(pid)
    GetWindowThreadProcessId(hwnd, p_pid)

    return OpenProcess(PROCESS_ALL_ACCESS, False, struct.unpack("i", pid)[0])


def get_desktop_icons_list():
    SendMessage = ctypes.windll.user32.SendMessageW
    VirtualAllocEx = ctypes.windll.kernel32.VirtualAllocEx
    WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory
    ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
    VirtualFreeEx = ctypes.windll.kernel32.VirtualFreeEx
    CloseHandle = ctypes.windll.kernel32.CloseHandle

    MAX_LEN = 4096

    icons_list = list()

    try:
        hwnd = GetDesktopListViewHandle()
        h_process = get_desktop_process_handle(hwnd)
        buffer_txt = VirtualAllocEx(
            h_process, 0, MAX_LEN, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE
        )

        copied = ctypes.create_string_buffer(4)
        p_copied = ctypes.addressof(copied)

        lvitem = LVITEMW()
        lvitem.mask = ctypes.c_uint32(LVIF_TEXT)
        lvitem.pszText = ctypes.c_uint64(buffer_txt)
        lvitem.cchTextMax = ctypes.c_int32(MAX_LEN)
        lvitem.iSubItem = ctypes.c_int32(0)

        p_buffer_lvi = VirtualAllocEx(
            h_process, 0, MAX_LEN, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE
        )
        WriteProcessMemory(
            h_process,
            p_buffer_lvi,
            ctypes.addressof(lvitem),
            ctypes.sizeof(LVITEMW),
            p_copied,
        )
        num_items = ListView_GetItemCount(hwnd)

        p_buffer_point = VirtualAllocEx(
            h_process, 0, ctypes.sizeof(POINT), MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE
        )
        p_buffer_rect = VirtualAllocEx(
            h_process, 0, ctypes.sizeof(RECT), MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE
        )

        for i in range(num_items):
            # Get icon text
            SendMessage(hwnd, LVM_GETITEMTEXT, i, p_buffer_lvi)
            target_bufftxt = ctypes.create_string_buffer(MAX_LEN)
            ReadProcessMemory(
                h_process,
                buffer_txt,
                ctypes.addressof(target_bufftxt),
                MAX_LEN,
                p_copied,
            )
            name = target_bufftxt.value.decode("cp1251")

            # Get icon position
            p = POINT()
            SendMessage(hwnd, LVM_GETITEMPOSITION, i, p_buffer_point)
            ReadProcessMemory(
                h_process,
                p_buffer_point,
                ctypes.addressof(p),
                ctypes.sizeof(POINT),
                p_copied,
            )

            rect = RECT()
            rect.left = LVIR_BOUNDS

            SendMessage(hwnd, LVM_GETITEMRECT, i, p_buffer_rect)
            ReadProcessMemory(
                h_process,
                p_buffer_rect,
                ctypes.addressof(rect),
                ctypes.sizeof(RECT),
                p_copied,
            )

            icons_list.append((i, name, p, rect))

    finally:
        try:
            VirtualFreeEx(h_process, p_buffer_lvi, 0, MEM_RELEASE)
        except:
            pass

        try:
            VirtualFreeEx(h_process, buffer_txt, 0, MEM_RELEASE)
        except:
            pass

        try:
            VirtualFreeEx(h_process, p_buffer_point, 0, MEM_RELEASE)
        except:
            pass

        try:
            VirtualFreeEx(h_process, p_buffer_rect, 0, MEM_RELEASE)
        except:
            pass

        try:
            CloseHandle(h_process)
        except:
            pass

    return icons_list


if __name__ == "__main__":
    icons_list = get_desktop_icons_list()

    # Сортировка по индексу
    for i, name, pos, rect in sorted(icons_list, key=lambda x: x[0]):
        print(
            f'{i + 1: >3}. "{name}": {pos.x}x{pos.y}, {rect.right - rect.left}x{rect.bottom - rect.top}'
        )
