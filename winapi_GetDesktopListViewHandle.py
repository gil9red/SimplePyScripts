#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


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

    import ctypes
    FindWindow = ctypes.windll.user32.FindWindowW
    GetWindow = ctypes.windll.user32.GetWindow
    GetClassName = ctypes.windll.user32.GetClassNameW
    GW_CHILD = 0x5

    def get_class_name(hwnd):
        buff = ctypes.create_unicode_buffer(100)
        GetClassName(hwnd, buff, 99)
        return buff.value

    # Ищем окно с классом "Progman" ("Program Manager")
    hwnd = FindWindow('Progman', None)

    # SHELLDLL_DefView
    hwnd = GetWindow(hwnd, GW_CHILD)

    # SysListView32
    hwnd = GetWindow(hwnd, GW_CHILD)

    if get_class_name(hwnd) != 'SysListView32':
        return 0

    return hwnd


if __name__ == '__main__':
    handle = GetDesktopListViewHandle()
    print('handle:', handle)
