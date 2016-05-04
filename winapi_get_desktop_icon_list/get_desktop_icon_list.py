#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import ctypes


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

    def GetClassName(hwnd):
        buff = ctypes.create_unicode_buffer(100)
        ctypes.windll.user32.GetClassNameW(hwnd, buff, 99)
        return buff.value

    from win32con import GW_CHILD

    # Ищем окно с классом "Progman" ("Program Manager")
    hwnd = FindWindow('Progman', None)
    hwnd = GetWindow(hwnd, GW_CHILD)  # SHELLDLL_DefView
    hwnd = GetWindow(hwnd, GW_CHILD)  # SysListView32

    if GetClassName(hwnd) != 'SysListView32':
        return 0

    return hwnd


def ListView_GetItemCount(hwnd):
    """

    Функция возвращает количество элементов указанного ListView.

    Оригинал:
    define ListView_GetItemCount(hwnd) (int)SNDMSG((hwnd),LVM_GETITEMCOUNT,(WPARAM)0,(LPARAM)0)

    """

    import commctrl
    import ctypes
    SendMessage = ctypes.windll.user32.SendMessageW

    return SendMessage(hwnd, commctrl.LVM_GETITEMCOUNT, 0, 0)


class LVITEMW(ctypes.Structure):
    _fields_ = [
        ('mask', ctypes.c_uint32),
        ('iItem', ctypes.c_int32),
        ('iSubItem', ctypes.c_int32),
        ('state', ctypes.c_uint32),
        ('stateMask', ctypes.c_uint32),
        ('pszText', ctypes.c_uint64),
        ('cchTextMax', ctypes.c_int32),
        ('iImage', ctypes.c_int32),
        ('lParam', ctypes.c_uint64),  # On 32 bit should be c_long
        ('iIndent', ctypes.c_int32),
        ('iGroupId', ctypes.c_int32),
        ('cColumns', ctypes.c_uint32),
        ('puColumns', ctypes.c_uint64),
        ('piColFmt', ctypes.c_int64),
        ('iGroup', ctypes.c_int32),
    ]


# TODO: исправить
# def ListView_GetItemRect(hwnd, i, rect, code=None):
#     """
#
#     Gets the bounding rectangle for all or part of an item in the current view.
#
#     Оригинал:
#     #define ListView_GetItemRect(hwnd,i,prc,code)
#     (WINBOOL) SNDMSG(
#         (hwnd),
#         LVM_GETITEMRECT,
#         (WPARAM)(int)(i),
#         ((prc) ? (((RECT *)(prc))->left = (code), (LPARAM)(RECT *)(prc)) : (LPARAM)(RECT *)NULL)
#     )
#
#     """
#
#     import commctrl
#     import ctypes
#     SendMessage = ctypes.windll.user32.SendMessageW
#
#     if code is None:
#         code = commctrl.LVIR_BOUNDS
#
#     rect.left = code
#     return SendMessage(hwnd, commctrl.LVM_GETITEMRECT, i, rect)


# Source: http://stackoverflow.com/q/28505766/5909792

# import ctypes
#
# class LVITEMW(ctypes.Structure):
#     _fields_ = [
#         ('mask', ctypes.c_uint32),
#         ('iItem', ctypes.c_int32),
#         ('iSubItem', ctypes.c_int32),
#         ('state', ctypes.c_uint32),
#         ('stateMask', ctypes.c_uint32),
#         ('pszText', ctypes.c_uint64),
#         ('cchTextMax', ctypes.c_int32),
#         ('iImage', ctypes.c_int32),
#         ('lParam', ctypes.c_uint64), # On 32 bit should be c_long
#         ('iIndent',ctypes.c_int32),
#         ('iGroupId', ctypes.c_int32),
#         ('cColumns', ctypes.c_uint32),
#         ('puColumns', ctypes.c_uint64),
#         ('piColFmt', ctypes.c_int64),
#         ('iGroup', ctypes.c_int32),
#     ]
#
# class POINT(ctypes.Structure):
#     _fields_ = [('x', ctypes.c_int), ('y', ctypes.c_int)]
#
# def icon_save_restore(savedicons=None, restore=False):
#     import struct, commctrl, win32gui, win32con, win32api
#     dthwnd = win32gui.FindWindow(None, 'Program Manager')
#     ukhwnd = win32gui.GetWindow(dthwnd, win32con.GW_CHILD)
#     slvhwnd = win32gui.GetWindow(ukhwnd, win32con.GW_CHILD)
#     pid = ctypes.create_string_buffer(4)
#     p_pid = ctypes.addressof(pid)
#     ctypes.windll.user32.GetWindowThreadProcessId(slvhwnd, p_pid)
#     hProcHnd = ctypes.windll.kernel32.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, struct.unpack("i",pid)[0])
#     pBuffertxt = ctypes.windll.kernel32.VirtualAllocEx(hProcHnd, 0, 4096, win32con.MEM_RESERVE|win32con.MEM_COMMIT, win32con.PAGE_READWRITE)
#     copied = ctypes.create_string_buffer(4)
#     p_copied = ctypes.addressof(copied)
#     lvitem = LVITEMW()
#     lvitem.mask = ctypes.c_uint32(commctrl.LVIF_TEXT)
#     lvitem.pszText = ctypes.c_uint64(pBuffertxt)
#     lvitem.cchTextMax = ctypes.c_int32(4096)
#     lvitem.iSubItem = ctypes.c_int32(0)
#     pLVI = ctypes.windll.kernel32.VirtualAllocEx(hProcHnd, 0, 4096, win32con.MEM_RESERVE| win32con.MEM_COMMIT,  win32con.PAGE_READWRITE)
#     win32api.SetLastError(0)
#     ctypes.windll.kernel32.WriteProcessMemory(hProcHnd, pLVI, ctypes.addressof(lvitem), ctypes.sizeof(lvitem), p_copied)
#     num_items = win32gui.SendMessage(slvhwnd, commctrl.LVM_GETITEMCOUNT)
#     if restore is False:
#         p = POINT()
#         pBufferpnt = ctypes.windll.kernel32.VirtualAllocEx(hProcHnd, 0, ctypes.sizeof(p), win32con.MEM_RESERVE|win32con.MEM_COMMIT, win32con.PAGE_READWRITE)
#         icons = {}
#         for i in xrange(num_items):
#             # Get icon text
#             win32gui.SendMessage(slvhwnd, commctrl.LVM_GETITEMTEXT, i, pLVI)
#             target_bufftxt = ctypes.create_string_buffer(4096)
#             ctypes.windll.kernel32.ReadProcessMemory(hProcHnd, pBuffertxt, ctypes.addressof(target_bufftxt), 4096, p_copied)
#             key = target_bufftxt.value
#             # Get icon position
#             win32api.SendMessage(slvhwnd, commctrl.LVM_GETITEMPOSITION, i, pBufferpnt)
#             p = POINT()
#             ctypes.windll.kernel32.ReadProcessMemory(hProcHnd, pBufferpnt, ctypes.addressof(p), ctypes.sizeof(p), p_copied)
#             icons[key] = (i,p)
#         ctypes.windll.kernel32.VirtualFreeEx(hProcHnd, pLVI, 0, win32con.MEM_RELEASE)
#         ctypes.windll.kernel32.VirtualFreeEx(hProcHnd, pBuffertxt, 0, win32con.MEM_RELEASE)
#         ctypes.windll.kernel32.VirtualFreeEx(hProcHnd, pBufferpnt, 0, win32con.MEM_RELEASE)
#         win32api.CloseHandle(hProcHnd)
#         return icons
#     else:  # RESTORE ICON POSITIONS PROBLEM IS HERE SOMEWHERE!!!
#         win32gui.SendMessage(slvhwnd, win32con.WM_SETREDRAW, 0, 0)
#         for i in xrange(num_items):
#             # Get icon text
#             win32gui.SendMessage(slvhwnd, commctrl.LVM_GETITEMTEXT, i, pLVI)
#             target_bufftxt = ctypes.create_string_buffer(4096)
#             ctypes.windll.kernel32.ReadProcessMemory(hProcHnd, pBuffertxt, ctypes.addressof(target_bufftxt), 4096, p_copied)
#             key = target_bufftxt.value
#             if key in savedicons.keys():
#                 # Set icon position
#                 p = savedicons[key][1]  # p is ctypes POINT
#                 p_lng = point_to_long(p)  # explicitly convert to HIWORD/LOWORD and c_long
#                 # Reserve space for input variable in foreign process and get pointer to it the that memory space
#                 pBufferpnt = ctypes.windll.kernel32.VirtualAllocEx(hProcHnd, 0, ctypes.sizeof(p_lng), win32con.MEM_RESERVE|win32con.MEM_COMMIT, win32con.PAGE_READWRITE)
#                 # Write the desired coordinates in to the space just created
#                 ret = ctypes.windll.kernel32.WriteProcessMemory(hProcHnd, pBufferpnt, ctypes.addressof(p_lng), ctypes.sizeof(p_lng), p_copied)
#                 if ret == 0:
#                     raise WindowsError
#                 # Send the message to change the position for that item's index and the pointer to the new position
#                 ret = win32gui.SendMessage(slvhwnd, commctrl.LVM_SETITEMPOSITION, i, pBufferpnt)
#                 if ret == 0:
#                     raise WindowsError
#                 # Release the reserved memory for the variable (I recognize that I probably don't need to aLloc/free this within the loop)
#                 ctypes.windll.kernel32.VirtualFreeEx(hProcHnd, pBufferpnt, 0, win32con.MEM_RELEASE)
#         win32gui.SendMessage(slvhwnd, win32con.WM_SETREDRAW, 1, 0)
#         ctypes.windll.kernel32.VirtualFreeEx(hProcHnd, pLVI, 0, win32con.MEM_RELEASE)
#         ctypes.windll.kernel32.VirtualFreeEx(hProcHnd, pBuffertxt, 0, win32con.MEM_RELEASE)
#         win32api.CloseHandle(hProcHnd)
#         return None
#
#
# def point_to_long(p):
#     ret = (p.y * 0x10000) + (p.x & 0xFFFF)
#     return ctypes.c_long(ret)
#
# if __name__ == '__main__':
#     mysavedicons = icon_save_restore(restore=False)
#     icon_save_restore(mysavedicons, restore=True)


def get_desktop_icons_list():
    import struct
    import ctypes
    from commctrl import LVIF_TEXT, LVM_GETITEMTEXT, LVM_GETITEMPOSITION, LVIR_BOUNDS, LVM_GETITEMRECT
    from win32con import PROCESS_ALL_ACCESS, MEM_RESERVE, MEM_COMMIT, PAGE_READWRITE, MEM_RELEASE
    from ctypes.wintypes import POINT, RECT

    GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
    SendMessage = ctypes.windll.user32.SendMessageW
    OpenProcess = ctypes.windll.kernel32.OpenProcess
    VirtualAllocEx = ctypes.windll.kernel32.VirtualAllocEx
    WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory
    ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
    VirtualFreeEx = ctypes.windll.kernel32.VirtualFreeEx
    CloseHandle = ctypes.windll.kernel32.CloseHandle

    MAX_LEN = 4096

    icons_list = list()

    try:
        hwnd = GetDesktopListViewHandle()
        pid = ctypes.create_string_buffer(4)
        p_pid = ctypes.addressof(pid)
        GetWindowThreadProcessId(hwnd, p_pid)

        h_process = OpenProcess(PROCESS_ALL_ACCESS, False, struct.unpack("i", pid)[0])
        buffer_txt = VirtualAllocEx(h_process, 0, MAX_LEN, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)

        copied = ctypes.create_string_buffer(4)
        p_copied = ctypes.addressof(copied)

        lvitem = LVITEMW()
        lvitem.mask = ctypes.c_uint32(LVIF_TEXT)
        lvitem.pszText = ctypes.c_uint64(buffer_txt)
        lvitem.cchTextMax = ctypes.c_int32(MAX_LEN)
        lvitem.iSubItem = ctypes.c_int32(0)

        p_buffer_lvi = VirtualAllocEx(h_process, 0, MAX_LEN, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)
        WriteProcessMemory(h_process, p_buffer_lvi, ctypes.addressof(lvitem), ctypes.sizeof(LVITEMW), p_copied)
        num_items = ListView_GetItemCount(hwnd)

        p_buffer_point = VirtualAllocEx(h_process, 0, ctypes.sizeof(POINT), MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)
        p_buffer_rect = VirtualAllocEx(h_process, 0, ctypes.sizeof(RECT), MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)

        for i in range(num_items):
            # Get icon text
            SendMessage(hwnd, LVM_GETITEMTEXT, i, p_buffer_lvi)
            target_bufftxt = ctypes.create_string_buffer(MAX_LEN)
            ReadProcessMemory(h_process, buffer_txt, ctypes.addressof(target_bufftxt), MAX_LEN, p_copied)
            name = target_bufftxt.value.decode('cp1251')

            # Get icon position
            p = POINT()
            SendMessage(hwnd, LVM_GETITEMPOSITION, i, p_buffer_point)
            ReadProcessMemory(h_process, p_buffer_point, ctypes.addressof(p), ctypes.sizeof(POINT), p_copied)

            rect = RECT()
            rect.left = LVIR_BOUNDS

            SendMessage(hwnd, LVM_GETITEMRECT, i, p_buffer_rect)
            ReadProcessMemory(h_process, p_buffer_rect, ctypes.addressof(rect), ctypes.sizeof(RECT), p_copied)

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


if __name__ == '__main__':
    icons_list = get_desktop_icons_list()

    # # Сортировка по положению на экране
    # for i, name, pos in sorted(icons_list, key=lambda x: (x[2].x, x[2].y)):
    #
    # # # Сортировка по индексу
    # for i, name, pos, rect in sorted(icons_list, key=lambda x: x[0]):
    #     print('{0: >3}. "{1}": {2.x}x{2.y}, {3.left}x{3.top} {3.right}x{3.bottom}'.format(i + 1, name, pos, rect))
    # # Сортировка по индексу
    for i, name, pos, rect in sorted(icons_list, key=lambda x: x[0]):
        print('{0: >3}. "{1}": {2.x}x{2.y}, {3}x{4}'.format(i + 1,
                                                            name,
                                                            pos,
                                                            rect.right - rect.left,
                                                            rect.bottom - rect.top,
                                                            ))

    # # # Сортировка по индексу
    # for i, name, pos in sorted(icons_list, key=lambda x: x[0]):
    #     print('{0: >3}. "{1}": {2.x}x{2.y}'.format(i + 1, name, pos))
