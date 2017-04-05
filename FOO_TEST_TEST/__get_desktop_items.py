#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# NOTE: set position icon
# SOURCE: http://webcache.googleusercontent.com/search?q=cache:GoDfFADI1_oJ:systools.losthost.org/%3Fcode%3D9+&cd=15&hl=ru&ct=clnk&client=firefox-b-ab
# SendMessage(lv, LVM_SETITEMPOSITION, i, MAKELONG(pt.x, pt.y));



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


# def get_desktop_icons_list():
#     import struct
#     import ctypes
#     from commctrl import LVIF_TEXT, LVIF_IMAGE, LVM_GETITEMTEXT, LVM_GETITEMPOSITION, LVIR_BOUNDS, LVM_GETITEMRECT, LVM_GETITEMW
#     from win32con import PROCESS_ALL_ACCESS, MEM_RESERVE, MEM_COMMIT, PAGE_READWRITE, MEM_RELEASE
#     from ctypes.wintypes import POINT, RECT
#
#     GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
#     SendMessage = ctypes.windll.user32.SendMessageW
#     OpenProcess = ctypes.windll.kernel32.OpenProcess
#     VirtualAllocEx = ctypes.windll.kernel32.VirtualAllocEx
#     WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory
#     ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
#     VirtualFreeEx = ctypes.windll.kernel32.VirtualFreeEx
#     CloseHandle = ctypes.windll.kernel32.CloseHandle
#
#     MAX_LEN = 4096
#
#     icons_list = list()
#
#     try:
#         hwnd = GetDesktopListViewHandle()
#         pid = ctypes.create_string_buffer(4)
#         p_pid = ctypes.addressof(pid)
#         GetWindowThreadProcessId(hwnd, p_pid)
#
#         h_process = OpenProcess(PROCESS_ALL_ACCESS, False, struct.unpack("i", pid)[0])
#         buffer_txt = VirtualAllocEx(h_process, 0, MAX_LEN, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)
#
#         copied = ctypes.create_string_buffer(4)
#         p_copied = ctypes.addressof(copied)
#
#         lvitem = LVITEMW()
#         lvitem.mask = ctypes.c_uint32(LVIF_TEXT | LVIF_IMAGE)
#         lvitem.iItem = ctypes.c_int32(0)
#         lvitem.iSubItem = ctypes.c_int32(0)
#         lvitem.pszText = ctypes.c_uint64(buffer_txt)
#         lvitem.cchTextMax = ctypes.c_int32(MAX_LEN)
#
#         p_buffer_lvi = VirtualAllocEx(h_process, 0, MAX_LEN, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)
#         WriteProcessMemory(h_process, p_buffer_lvi, ctypes.addressof(lvitem), ctypes.sizeof(LVITEMW), p_copied)
#
#         p_buffer_point = VirtualAllocEx(h_process, 0, ctypes.sizeof(POINT), MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)
#         p_buffer_rect = VirtualAllocEx(h_process, 0, ctypes.sizeof(RECT), MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)
#
#         num_items = ListView_GetItemCount(hwnd)
#
#         for i in range(num_items):
#             # Get icon text
#             SendMessage(hwnd, LVM_GETITEMTEXT, i, p_buffer_lvi)
#             target_bufftxt = ctypes.create_string_buffer(MAX_LEN)
#             ReadProcessMemory(h_process, buffer_txt, ctypes.addressof(target_bufftxt), MAX_LEN, p_copied)
#             name = target_bufftxt.value.decode('cp1251')
#             print(name)
#
#             lvitem.iItem = ctypes.c_int32(i)
#             p_buffer_lvi = VirtualAllocEx(h_process, 0, MAX_LEN, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)
#             WriteProcessMemory(h_process, p_buffer_lvi, ctypes.addressof(lvitem), ctypes.sizeof(LVITEMW), p_copied)
#
#             SendMessage(hwnd, LVM_GETITEMW, 0, p_buffer_lvi)
#             ReadProcessMemory(h_process, p_buffer_lvi, ctypes.addressof(lvitem), ctypes.sizeof(LVITEMW), p_copied)
#             print(lvitem.iImage)
#             # quit()
#
#             # Get icon position
#             p = POINT()
#             SendMessage(hwnd, LVM_GETITEMPOSITION, i, p_buffer_point)
#             ReadProcessMemory(h_process, p_buffer_point, ctypes.addressof(p), ctypes.sizeof(POINT), p_copied)
#
#             rect = RECT()
#             rect.left = LVIR_BOUNDS
#
#             SendMessage(hwnd, LVM_GETITEMRECT, i, p_buffer_rect)
#             ReadProcessMemory(h_process, p_buffer_rect, ctypes.addressof(rect), ctypes.sizeof(RECT), p_copied)
#
#             print(name)
#             # icons_list.append((i, name, p, rect))
#
#     finally:
#         try:
#             VirtualFreeEx(h_process, p_buffer_lvi, 0, MEM_RELEASE)
#         except:
#             pass
#
#         try:
#             VirtualFreeEx(h_process, buffer_txt, 0, MEM_RELEASE)
#         except:
#             pass
#
#         try:
#             VirtualFreeEx(h_process, p_buffer_point, 0, MEM_RELEASE)
#         except:
#             pass
#
#         try:
#             VirtualFreeEx(h_process, p_buffer_rect, 0, MEM_RELEASE)
#         except:
#             pass
#
#         try:
#             CloseHandle(h_process)
#         except:
#             pass
#
#     return icons_list


def get_desktop_image_icon(index):
    import struct
    import ctypes
    from commctrl import LVIF_IMAGE, LVM_GETITEMW
    from win32con import PROCESS_ALL_ACCESS, MEM_RESERVE, MEM_COMMIT, PAGE_READWRITE, MEM_RELEASE

    GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
    SendMessage = ctypes.windll.user32.SendMessageW
    OpenProcess = ctypes.windll.kernel32.OpenProcess
    VirtualAllocEx = ctypes.windll.kernel32.VirtualAllocEx
    WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory
    ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
    VirtualFreeEx = ctypes.windll.kernel32.VirtualFreeEx
    CloseHandle = ctypes.windll.kernel32.CloseHandle

    MAX_LEN = 4096

    try:
        hwnd = GetDesktopListViewHandle()
        pid = ctypes.create_string_buffer(4)
        p_pid = ctypes.addressof(pid)
        GetWindowThreadProcessId(hwnd, p_pid)

        h_process = OpenProcess(PROCESS_ALL_ACCESS, False, struct.unpack("i", pid)[0])

        copied = ctypes.create_string_buffer(4)
        p_copied = ctypes.addressof(copied)

        lvitem = LVITEMW()
        lvitem.mask = ctypes.c_uint32(LVIF_IMAGE)
        lvitem.iItem = ctypes.c_int32(index)
        lvitem.iSubItem = ctypes.c_int32(0)

        p_buffer_lvi = VirtualAllocEx(h_process, 0, MAX_LEN, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)
        WriteProcessMemory(h_process, p_buffer_lvi, ctypes.addressof(lvitem), ctypes.sizeof(LVITEMW), p_copied)

        SendMessage(hwnd, LVM_GETITEMW, 0, p_buffer_lvi)
        ReadProcessMemory(h_process, p_buffer_lvi, ctypes.addressof(lvitem), ctypes.sizeof(LVITEMW), p_copied)
        return lvitem.iImage

    finally:
        try:
            VirtualFreeEx(h_process, p_buffer_lvi, 0, MEM_RELEASE)
        except:
            pass

        try:
            CloseHandle(h_process)
        except:
            pass


def ListView_GetImageList(hwnd, i_image_list):
    """

    Gets the handle to an image list used for drawing list-view items. You can use this macro or send the LVM_GETIMAGELIST message explicitly.

    Original:
    #define ListView_GetImageList(w,i) (HIMAGELIST)SNDMSG((w),LVM_GETIMAGELIST,(i),0)

    :param hwnd:
    :param i_image_list:
    :return:
    """

    import ctypes
    SendMessage = ctypes.windll.user32.SendMessageW

    from commctrl import LVM_GETIMAGELIST

    return SendMessage(hwnd, LVM_GETIMAGELIST, i_image_list, 0)


print(get_desktop_image_icon(0))  # 11
print(get_desktop_image_icon(1))  # 12
print(get_desktop_image_icon(2))  # 13

hwnd = GetDesktopListViewHandle()
print(hwnd)  # 65784

from commctrl import LVSIL_NORMAL, ILD_IMAGE
h_il = ListView_GetImageList(hwnd, LVSIL_NORMAL)
print(h_il)  # 860139888

from win32gui import ImageList_GetIcon
print(ImageList_GetIcon(h_il, 0, ILD_IMAGE))  # 0
print(ImageList_GetIcon(h_il, 11, ILD_IMAGE))  # 0


# typedef struct _IMAGEINFO {
#   HBITMAP hbmImage;
#   HBITMAP hbmMask;
#   int     Unused1;
#   int     Unused2;
#   RECT    rcImage;
# } IMAGEINFO, *LPIMAGEINFO;

import ctypes.wintypes
class IMAGEINFO(ctypes.Structure):
    _fields_ = [
        ('hbmImage', ctypes.wintypes.HBITMAP),
        ('hbmMask', ctypes.wintypes.HBITMAP),
        ('Unused1', ctypes.c_int),
        ('Unused2', ctypes.c_int),
        ('rcImage', ctypes.wintypes.RECT),
    ]

ImageList_GetImageInfo = ctypes.windll.comctl32.ImageList_GetImageInfo
# BOOL ImageList_GetImageInfo(
#    HIMAGELIST himl,
#    int        i,
#    IMAGEINFO  *pImageInfo
# );

pImageInfo = IMAGEINFO()
print(ImageList_GetImageInfo(h_il, 0, ctypes.byref(pImageInfo)))  # 0
print(ImageList_GetImageInfo(h_il, 11, ctypes.byref(pImageInfo)))  # 0




# import struct
#
# from PIL import Image
# from PIL.ImageOps import flip
#
# import ctypes
# from ctypes import wintypes
# windll = ctypes.windll
# user32 = windll.user32
# gdi32 = windll.gdi32
#
#
# class RECT(ctypes.Structure):
#     _fields_ = [
#         ('left', ctypes.c_long),
#         ('top', ctypes.c_long),
#         ('right', ctypes.c_long),
#         ('bottom', ctypes.c_long)
#     ]
#
#
# class BITMAPINFOHEADER(ctypes.Structure):
#     _fields_ = [
#         ("biSize", wintypes.DWORD),
#         ("biWidth", ctypes.c_long),
#         ("biHeight", ctypes.c_long),
#         ("biPlanes", wintypes.WORD),
#         ("biBitCount", wintypes.WORD),
#         ("biCompression", wintypes.DWORD),
#         ("biSizeImage", wintypes.DWORD),
#         ("biXPelsPerMeter", ctypes.c_long),
#         ("biYPelsPerMeter", ctypes.c_long),
#         ("biClrUsed", wintypes.DWORD),
#         ("biClrImportant", wintypes.DWORD)
#     ]
#
#
# class BITMAPINFO(ctypes.Structure):
#     _fields_ = [
#         ("bmiHeader", BITMAPINFOHEADER)
#     ]
#
#
# class BITMAP(ctypes.Structure):
#     _fields_ = [
#         ("bmType", ctypes.c_long),
#         ("bmWidth", ctypes.c_long),
#         ("bmHeight", ctypes.c_long),
#         ("bmWidthBytes", ctypes.c_long),
#         ("bmPlanes", wintypes.WORD),
#         ("bmBitsPixel", wintypes.WORD),
#         ("bmBits", ctypes.c_void_p)
#     ]
#
#
# def get_window_image(whandle):
#     def round_up32(n):
#         multiple = 32
#
#         while multiple < n:
#             multiple += 32
#
#         return multiple
#
#     rect = RECT()
#     user32.GetClientRect(whandle, ctypes.byref(rect))
#     bbox = (rect.left, rect.top, rect.right, rect.bottom)
#
#     hdcScreen = user32.GetDC(None)
#     hdc = gdi32.CreateCompatibleDC(hdcScreen)
#     hbmp = gdi32.CreateCompatibleBitmap(
#         hdcScreen,
#         bbox[2] - bbox[0],
#         bbox[3] - bbox[1]
#     )
#     gdi32.SelectObject(hdc, hbmp)
#
#     PW_CLIENTONLY = 1
#
#     if not user32.PrintWindow(whandle, hdc, PW_CLIENTONLY):
#         raise Exception("PrintWindow failed")
#
#     bmap = BITMAP()
#     if not gdi32.GetObjectW(hbmp, ctypes.sizeof(BITMAP), ctypes.byref(bmap)):
#         raise Exception("GetObject failed")
#
#     if bmap.bmBitsPixel != 32:
#         raise Exception("WTF")
#
#     scanline_len = round_up32(bmap.bmWidth * bmap.bmBitsPixel)
#     data_len = scanline_len * bmap.bmHeight
#
#     # http://msdn.microsoft.com/en-us/library/ms969901.aspx
#     bminfo = BITMAPINFO()
#     bminfo.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
#     bminfo.bmiHeader.biWidth = bmap.bmWidth
#     bminfo.bmiHeader.biHeight = bmap.bmHeight
#     bminfo.bmiHeader.biPlanes = 1
#     bminfo.bmiHeader.biBitCount = 24  # bmap.bmBitsPixel
#     bminfo.bmiHeader.biCompression = 0
#
#     data = ctypes.create_string_buffer(data_len)
#
#     DIB_RGB_COLORS = 0
#
#     get_bits_success = gdi32.GetDIBits(
#         hdc, hbmp,
#         0, bmap.bmHeight,
#         ctypes.byref(data), ctypes.byref(bminfo),
#         DIB_RGB_COLORS
#     )
#     if not get_bits_success:
#         raise Exception("GetDIBits failed")
#
#     # http://msdn.microsoft.com/en-us/library/dd183376%28v=vs.85%29.aspx
#     bmiheader_fmt = "LllHHLLllLL"
#
#     unpacked_header = [
#         bminfo.bmiHeader.biSize,
#         bminfo.bmiHeader.biWidth,
#         bminfo.bmiHeader.biHeight,
#         bminfo.bmiHeader.biPlanes,
#         bminfo.bmiHeader.biBitCount,
#         bminfo.bmiHeader.biCompression,
#         bminfo.bmiHeader.biSizeImage,
#         bminfo.bmiHeader.biXPelsPerMeter,
#         bminfo.bmiHeader.biYPelsPerMeter,
#         bminfo.bmiHeader.biClrUsed,
#         bminfo.bmiHeader.biClrImportant
#     ]
#
#     # Indexes: biXPelsPerMeter = 7, biYPelsPerMeter = 8
#     # Value from http://stackoverflow.com/a/23982267/2065904
#     unpacked_header[7] = 3779
#     unpacked_header[8] = 3779
#
#     image_header = struct.pack(bmiheader_fmt, *unpacked_header)
#
#     image = image_header + data
#
#     return flip(Image.frombytes("RGB", (bmap.bmWidth, bmap.bmHeight), image))
#
# import ctypes
#
# def GetDesktopListViewHandle():
#     """
#     Функция возвращает указатель на ListView рабочего стола.
#
#     Оригинал:
#     function GetDesktopListViewHandle: THandle;
#         var
#             S: string;
#         begin
#             Result := FindWindow('ProgMan', nil);
#             Result := GetWindow(Result, GW_CHILD);
#             Result := GetWindow(Result, GW_CHILD);
#             SetLength(S, 40);
#             GetClassName(Result, PChar(S), 39);
#             if PChar(S) <> 'SysListView32' then
#                 Result := 0;
#         end;
#
#     """
#
#     import ctypes
#     FindWindow = ctypes.windll.user32.FindWindowW
#     GetWindow = ctypes.windll.user32.GetWindow
#
#     def GetClassName(hwnd):
#         buff = ctypes.create_unicode_buffer(100)
#         ctypes.windll.user32.GetClassNameW(hwnd, buff, 99)
#         return buff.value
#
#     from win32con import GW_CHILD
#
#     # Ищем окно с классом "Progman" ("Program Manager")
#     hwnd = FindWindow('Progman', None)
#     hwnd = GetWindow(hwnd, GW_CHILD)  # SHELLDLL_DefView
#     hwnd = GetWindow(hwnd, GW_CHILD)  # SysListView32
#
#     if GetClassName(hwnd) != 'SysListView32':
#         return 0
#
#     return hwnd
#
# im = get_window_image(GetDesktopListViewHandle())
# print(im)
# im.show()
#
# quit()

# import ctypes
#
# def GetDesktopListViewHandle():
#     """
#     Функция возвращает указатель на ListView рабочего стола.
#
#     Оригинал:
#     function GetDesktopListViewHandle: THandle;
#         var
#             S: string;
#         begin
#             Result := FindWindow('ProgMan', nil);
#             Result := GetWindow(Result, GW_CHILD);
#             Result := GetWindow(Result, GW_CHILD);
#             SetLength(S, 40);
#             GetClassName(Result, PChar(S), 39);
#             if PChar(S) <> 'SysListView32' then
#                 Result := 0;
#         end;
#
#     """
#
#     import ctypes
#     FindWindow = ctypes.windll.user32.FindWindowW
#     GetWindow = ctypes.windll.user32.GetWindow
#
#     def GetClassName(hwnd):
#         buff = ctypes.create_unicode_buffer(100)
#         ctypes.windll.user32.GetClassNameW(hwnd, buff, 99)
#         return buff.value
#
#     from win32con import GW_CHILD
#
#     # Ищем окно с классом "Progman" ("Program Manager")
#     hwnd = FindWindow('Progman', None)
#     hwnd = GetWindow(hwnd, GW_CHILD)  # SHELLDLL_DefView
#     hwnd = GetWindow(hwnd, GW_CHILD)  # SysListView32
#
#     if GetClassName(hwnd) != 'SysListView32':
#         return 0
#
#     return hwnd
#
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
#         ('lParam', ctypes.c_uint64),  # On 32 bit should be c_long
#         ('iIndent', ctypes.c_int32),
#         ('iGroupId', ctypes.c_int32),
#         ('cColumns', ctypes.c_uint32),
#         ('puColumns', ctypes.c_uint64),
#         ('piColFmt', ctypes.c_int64),
#         ('iGroup', ctypes.c_int32),
#     ]
#
#
# def get_desktop_process_handle(hwnd=None):
#     import ctypes
#     import struct
#     from win32con import PROCESS_ALL_ACCESS
#
#     GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
#     OpenProcess = ctypes.windll.kernel32.OpenProcess
#
#     if hwnd is None:
#         hwnd = GetDesktopListViewHandle()
#
#     pid = ctypes.create_string_buffer(4)
#     p_pid = ctypes.addressof(pid)
#     GetWindowThreadProcessId(hwnd, p_pid)
#
#     return OpenProcess(PROCESS_ALL_ACCESS, False, struct.unpack("i", pid)[0])
#
#
# def get_desktop_image_icon(index):
#     import ctypes
#     from commctrl import LVIF_IMAGE, LVM_GETITEMW
#     from win32con import MEM_RESERVE, MEM_COMMIT, PAGE_READWRITE, MEM_RELEASE
#
#     SendMessage = ctypes.windll.user32.SendMessageW
#     VirtualAllocEx = ctypes.windll.kernel32.VirtualAllocEx
#     WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory
#     ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
#     VirtualFreeEx = ctypes.windll.kernel32.VirtualFreeEx
#     CloseHandle = ctypes.windll.kernel32.CloseHandle
#
#     MAX_LEN = 4096
#
#     try:
#         hwnd = GetDesktopListViewHandle()
#         h_process = get_desktop_process_handle(hwnd)
#
#         copied = ctypes.create_string_buffer(4)
#         p_copied = ctypes.addressof(copied)
#
#         lvitem = LVITEMW()
#         lvitem.mask = ctypes.c_uint32(LVIF_IMAGE)
#         lvitem.iItem = ctypes.c_int32(index)
#         lvitem.iSubItem = ctypes.c_int32(0)
#
#         p_buffer_lvi = VirtualAllocEx(h_process, 0, MAX_LEN, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)
#         WriteProcessMemory(h_process, p_buffer_lvi, ctypes.addressof(lvitem), ctypes.sizeof(LVITEMW), p_copied)
#
#         SendMessage(hwnd, LVM_GETITEMW, 0, p_buffer_lvi)
#         ReadProcessMemory(h_process, p_buffer_lvi, ctypes.addressof(lvitem), ctypes.sizeof(LVITEMW), p_copied)
#         return lvitem.iImage
#
#     finally:
#         try:
#             VirtualFreeEx(h_process, p_buffer_lvi, 0, MEM_RELEASE)
#         except:
#             pass
#
#         try:
#             CloseHandle(h_process)
#         except:
#             pass
#
#
# # h_process = get_desktop_process_handle()
# # print(h_process)
#
# # LoadImage = ctypes.windll.user32.LoadImageW
#
# # ctypes.wintypes.windll.user32.LoadImageW(defs.NULL, unicode(icon, 'mbcs'), defs.IMAGE_ICON, 0, 0, defs.LR_LOADFROMFILE);
# # LoadImage = ctypes.wintypes.windll.user32.LoadImageW
# #
# # LoadImage
# # _In_opt_ HINSTANCE hinst,
# # _In_     LPCTSTR   lpszName,
# # _In_     UINT      uType,
# # _In_     int       cxDesired,
# # _In_     int       cyDesired,
# # _In_     UINT      fuLoad
#
# # hBitmap =(HBITMAP)LoadImage(NULL,"C:\\test.bmp",IMAGE_BITMAP,0,0,LR_LOADFROMFILE);
#
#
# # def MAKEINTRESOURCE(i):
# #     """
# #
# #     #define MAKEINTRESOURCEW(i) ((LPWSTR)((ULONG_PTR)((WORD)(i))))
# #     """
# #
# #     return str(hex(i))
# #
# # from win32gui import IMAGE_BITMAP, LR_DEFAULTSIZE, ImageList_GetIcon
# # print(MAKEINTRESOURCE(id_image))
# # # h_bitmap = LoadImage(h_process, MAKEINTRESOURCE(id_image), IMAGE_IC, LR_DEFAULTSIZE, LR_DEFAULTSIZE, LR_DEFAULTSIZE)
# # # print(h_bitmap)
#
#
# def ListView_GetImageList(hwnd, i_image_list):
#     """
#
#     This retrieves the handle to an image list used for drawing list-view items.
#     You can use this or send the LVM_GETIMAGELIST message explicitly.
#
#     Original:
#     #define ListView_GetImageList(w,i) (HIMAGELIST)SNDMSG((w),LVM_GETIMAGELIST,(i),0)
#
#     :param hwnd: Handle to the list-view control.
#     :param i_image_list: Image list to retrieve. It is one of the following values.
#         Value	Description
#         LVSIL_NORMAL Image list with large icons. (LVSIL_NORMAL = 0)
#         LVSIL_SMALL	Image list with small icons. (LVSIL_SMALL = 1)
#         LVSIL_STATE	Image list with state images. (LVSIL_STATE = 2)
#     :return:
#     """
#
#     import ctypes
#     SendMessage = ctypes.windll.user32.SendMessageW
#
#     from commctrl import LVM_GETIMAGELIST
#
#     return SendMessage(hwnd, LVM_GETIMAGELIST, i_image_list, 0)
#
#
# from commctrl import LVSIL_NORMAL
# hwnd = GetDesktopListViewHandle()
# print(hwnd)
#
# # h_process = get_desktop_process_handle(hwnd)
# # print(h_process)
#
# himl = ListView_GetImageList(hwnd, LVSIL_NORMAL)
# print(himl)
#
# id_image = get_desktop_image_icon(0)
# print(id_image)
#
# from win32gui import ImageList_GetIcon, ILD_NORMAL, ILD_TRANSPARENT, DestroyIcon
# h_icon = ImageList_GetIcon(himl, id_image, ILD_NORMAL | ILD_TRANSPARENT)
# h_icon = ImageList_GetIcon(himl, id_image, ILD_NORMAL)
# print(h_icon)


# winapi_qt_get_icon_file_name.py



# ImageList_GetIconSize = ctypes.windll.comctl32.ImageList_GetIconSize
# # ImageList_ExtractIcon = ctypes.windll.comctl32.ImageList_ExtractIcon
# cx = ctypes.c_int()
# cy = ctypes.c_int()
# print(ImageList_GetIconSize(himl, ctypes.byref(cx), ctypes.byref(cy)), cx, cy)
# # from win32gui import ImageList_GetIconSize

# px = QPixmap.fromWinHICON(hIcon)
# DestroyIcon(hIcon)

# print(LoadImage(defs.NULL, unicode(icon, 'mbcs'), defs.IMAGE_ICON, 0, 0, defs.LR_LOADFROMFILE))



def get_desktop_image_icon(index):
    import struct
    import ctypes
    from commctrl import LVIF_IMAGE, LVM_GETITEMW
    from win32con import PROCESS_ALL_ACCESS, MEM_RESERVE, MEM_COMMIT, PAGE_READWRITE, MEM_RELEASE

    GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
    SendMessage = ctypes.windll.user32.SendMessageW
    OpenProcess = ctypes.windll.kernel32.OpenProcess
    VirtualAllocEx = ctypes.windll.kernel32.VirtualAllocEx
    WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory
    ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
    VirtualFreeEx = ctypes.windll.kernel32.VirtualFreeEx
    CloseHandle = ctypes.windll.kernel32.CloseHandle

    MAX_LEN = 4096

    try:
        hwnd = GetDesktopListViewHandle()
        pid = ctypes.create_string_buffer(4)
        p_pid = ctypes.addressof(pid)
        GetWindowThreadProcessId(hwnd, p_pid)

        h_process = OpenProcess(PROCESS_ALL_ACCESS, False, struct.unpack("i", pid)[0])

        copied = ctypes.create_string_buffer(4)
        p_copied = ctypes.addressof(copied)

        lvitem = LVITEMW()
        lvitem.mask = ctypes.c_uint32(LVIF_IMAGE)
        lvitem.iItem = ctypes.c_int32(index)
        lvitem.iSubItem = ctypes.c_int32(0)

        p_buffer_lvi = VirtualAllocEx(h_process, 0, MAX_LEN, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE)
        WriteProcessMemory(h_process, p_buffer_lvi, ctypes.addressof(lvitem), ctypes.sizeof(LVITEMW), p_copied)

        SendMessage(hwnd, LVM_GETITEMW, 0, p_buffer_lvi)
        ReadProcessMemory(h_process, p_buffer_lvi, ctypes.addressof(lvitem), ctypes.sizeof(LVITEMW), p_copied)
        return lvitem.iImage

    finally:
        try:
            VirtualFreeEx(h_process, p_buffer_lvi, 0, MEM_RELEASE)
        except:
            pass

        try:
            CloseHandle(h_process)
        except:
            pass
