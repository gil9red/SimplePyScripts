#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import ctypes
from ctypes import wintypes

from PySide.QtGui import QApplication, QImage

from win32gui import DestroyIcon, DrawIconEx, GetIconInfo


def get_file_icon(path, large=True):
    SHGetFileInfo = ctypes.windll.shell32.SHGetFileInfoW

    SHGFI_ICON = 0x100
    SHGFI_SYSICONINDEX = 0x4000
    SHGFI_LARGEICON = 0x0
    SHGFI_SMALLICON = 0x1

    class SHFILEINFO(ctypes.Structure):
        _fields_ = [
            ("hIcon", ctypes.c_void_p),
            ("iIcon", ctypes.c_int32),
            ("dwAttributes", ctypes.c_uint32),
            ("szDisplayName", ctypes.c_wchar * 260),
            ("szTypeName", ctypes.c_wchar * 80),
        ]

    info = SHFILEINFO()
    flags = SHGFI_ICON | SHGFI_SYSICONINDEX
    flags |= SHGFI_LARGEICON if large else SHGFI_SMALLICON

    COINIT_APARTMENTTHREADED = 0x2
    COINIT_DISABLE_OLE1DDE = 0x4
    CoInitializeEx = ctypes.windll.ole32.CoInitializeEx
    CoInitializeEx(None, COINIT_APARTMENTTHREADED | COINIT_DISABLE_OLE1DDE)

    rc = SHGetFileInfo(path, 0, ctypes.byref(info), ctypes.sizeof(info), flags)
    if not rc and info.iIcon:
        return

    return info.hIcon


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", wintypes.DWORD),
        ("biWidth", ctypes.c_long),
        ("biHeight", ctypes.c_long),
        ("biPlanes", wintypes.WORD),
        ("biBitCount", wintypes.WORD),
        ("biCompression", wintypes.DWORD),
        ("biSizeImage", wintypes.DWORD),
        ("biXPelsPerMeter", ctypes.c_long),
        ("biYPelsPerMeter", ctypes.c_long),
        ("biClrUsed", wintypes.DWORD),
        ("biClrImportant", wintypes.DWORD),
    ]


class BITMAPINFO(ctypes.Structure):
    _fields_ = [("bmiHeader", BITMAPINFOHEADER)]


def qt_fromWinHBITMAP(hdc, h_bitmap, w, h):
    """

    Original:
    static QImage qt_fromWinHBITMAP(HDC hdc, HBITMAP bitmap, int w, int h)
    {
        BITMAPINFO bmi;
        memset(&bmi, 0, sizeof(bmi));
        bmi.bmiHeader.biSize        = sizeof(BITMAPINFOHEADER);
        bmi.bmiHeader.biWidth       = w;
        bmi.bmiHeader.biHeight      = -h;
        bmi.bmiHeader.biPlanes      = 1;
        bmi.bmiHeader.biBitCount    = 32;
        bmi.bmiHeader.biCompression = BI_RGB;
        bmi.bmiHeader.biSizeImage   = w * h * 4;

        QImage image(w, h, QImage::Format_ARGB32_Premultiplied);
        if (image.isNull())
            return image;

        // Get bitmap bits
        uchar *data = (uchar *) qMalloc(bmi.bmiHeader.biSizeImage);

        if (GetDIBits(hdc, bitmap, 0, h, data, &bmi, DIB_RGB_COLORS)) {
            // Create image and copy data into image.
            for (int y=0; y<h; ++y) {
                void *dest = (void *) image.scanLine(y);
                void *src = data + y * image.bytesPerLine();
                memcpy(dest, src, image.bytesPerLine());
            }
        } else {
            qWarning("qt_fromWinHBITMAP(), failed to get bitmap bits");
        }
        qFree(data);

        return image;
    }
    """

    GetDIBits = ctypes.windll.gdi32.GetDIBits
    DIB_RGB_COLORS = 0
    BI_RGB = 0

    bitmapInfo = BITMAPINFO()
    bitmapInfo.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bitmapInfo.bmiHeader.biWidth = w
    bitmapInfo.bmiHeader.biHeight = -h
    bitmapInfo.bmiHeader.biPlanes = 1
    bitmapInfo.bmiHeader.biBitCount = 32
    bitmapInfo.bmiHeader.biCompression = BI_RGB
    bitmapInfo.bmiHeader.biSizeImage = w * h * 4

    image = QImage(w, h, QImage.Format_ARGB32_Premultiplied)
    if image.isNull():
        return image

    # Get bitmap bits
    data = ctypes.create_string_buffer(bitmapInfo.bmiHeader.biSizeImage)

    if GetDIBits(
        hdc,
        h_bitmap,
        0,
        h,
        ctypes.byref(data),
        ctypes.byref(bitmapInfo),
        DIB_RGB_COLORS,
    ):
        # Create image and copy data into image.
        for y in range(h):
            dest = image.scanLine(y)

            src = data[
                y * image.bytesPerLine() : y * image.bytesPerLine()
                + image.bytesPerLine()
            ]
            for i in range(image.bytesPerLine()):
                dest[i] = src[i]

    else:
        # qWarning("qt_fromWinHBITMAP(), failed to get bitmap bits");
        print("qt_fromWinHBITMAP(), failed to get bitmap bits")

    return image


def fromWinHICON(h_icon):
    """

    Original:
    QPixmap QPixmap::fromWinHICON(HICON icon)
    {
        bool foundAlpha = false;
        HDC screenDevice = GetDC(0);
        HDC hdc = CreateCompatibleDC(screenDevice);
        ReleaseDC(0, screenDevice);

        ICONINFO iconinfo;
        bool result = GetIconInfo(icon, &iconinfo); //x and y Hotspot describes the icon center
        if (!result)
            qWarning("QPixmap::fromWinHICON(), failed to GetIconInfo()");

        int w = iconinfo.xHotspot * 2;
        int h = iconinfo.yHotspot * 2;

        BITMAPINFOHEADER bitmapInfo;
        bitmapInfo.biSize        = sizeof(BITMAPINFOHEADER);
        bitmapInfo.biWidth       = w;
        bitmapInfo.biHeight      = h;
        bitmapInfo.biPlanes      = 1;
        bitmapInfo.biBitCount    = 32;
        bitmapInfo.biCompression = BI_RGB;
        bitmapInfo.biSizeImage   = 0;
        bitmapInfo.biXPelsPerMeter = 0;
        bitmapInfo.biYPelsPerMeter = 0;
        bitmapInfo.biClrUsed       = 0;
        bitmapInfo.biClrImportant  = 0;
        DWORD* bits;

        HBITMAP winBitmap = CreateDIBSection(hdc, (BITMAPINFO*)&bitmapInfo, DIB_RGB_COLORS, (VOID**)&bits, NULL, 0);
        HGDIOBJ oldhdc = (HBITMAP)SelectObject(hdc, winBitmap);
        DrawIconEx( hdc, 0, 0, icon, iconinfo.xHotspot * 2, iconinfo.yHotspot * 2, 0, 0, DI_NORMAL);
        QImage image = qt_fromWinHBITMAP(hdc, winBitmap, w, h);

        for (int y = 0 ; y < h && !foundAlpha ; y++) {
            QRgb *scanLine= reinterpret_cast<QRgb *>(image.scanLine(y));
            for (int x = 0; x < w ; x++) {
                if (qAlpha(scanLine[x]) != 0) {
                    foundAlpha = true;
                    break;
                }
            }
        }
        if (!foundAlpha) {
            //If no alpha was found, we use the mask to set alpha values
            DrawIconEx( hdc, 0, 0, icon, w, h, 0, 0, DI_MASK);
            QImage mask = qt_fromWinHBITMAP(hdc, winBitmap, w, h);

            for (int y = 0 ; y < h ; y++){
                QRgb *scanlineImage = reinterpret_cast<QRgb *>(image.scanLine(y));
                QRgb *scanlineMask = mask.isNull() ? 0 : reinterpret_cast<QRgb *>(mask.scanLine(y));
                for (int x = 0; x < w ; x++){
                    if (scanlineMask && qRed(scanlineMask[x]) != 0)
                        scanlineImage[x] = 0; //mask out this pixel
                    else
                        scanlineImage[x] |= 0xff000000; // set the alpha channel to 255
                }
            }
        }
        //dispose resources created by iconinfo call
        DeleteObject(iconinfo.hbmMask);
        DeleteObject(iconinfo.hbmColor);

        SelectObject(hdc, oldhdc); //restore state
        DeleteObject(winBitmap);
        DeleteDC(hdc);
        return QPixmap::fromImage(image);
    }
    """

    BI_RGB = 0

    GetDC = ctypes.windll.user32.GetDC
    ReleaseDC = ctypes.windll.user32.ReleaseDC
    DeleteDC = ctypes.windll.gdi32.DeleteDC

    CreateCompatibleDC = ctypes.windll.gdi32.CreateCompatibleDC
    CreateDIBSection = ctypes.windll.gdi32.CreateDIBSection
    SelectObject = ctypes.windll.gdi32.SelectObject
    DeleteObject = ctypes.windll.gdi32.DeleteObject

    # foundAlpha = False
    screenDevice = GetDC(0)
    hdc = CreateCompatibleDC(screenDevice)
    ReleaseDC(0, screenDevice)

    iconinfo = GetIconInfo(h_icon)
    flag, xHotspot, yHotspot, hbmMask, hbmColor = iconinfo

    w = xHotspot * 2
    h = yHotspot * 2

    bitmapInfo = BITMAPINFO()
    bitmapInfo.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bitmapInfo.bmiHeader.biWidth = w
    bitmapInfo.bmiHeader.biHeight = h
    bitmapInfo.bmiHeader.biPlanes = 1
    bitmapInfo.bmiHeader.biBitCount = 32
    bitmapInfo.bmiHeader.biCompression = BI_RGB
    bitmapInfo.bmiHeader.biSizeImage = 0
    bitmapInfo.bmiHeader.biXPelsPerMeter = 0
    bitmapInfo.bmiHeader.biYPelsPerMeter = 0
    bitmapInfo.bmiHeader.biClrUsed = 0
    bitmapInfo.bmiHeader.biClrImportant = 0

    DIB_RGB_COLORS = 0

    winBitmap = CreateDIBSection(hdc, ctypes.byref(bitmapInfo), DIB_RGB_COLORS, 0, 0, 0)
    oldhdc = SelectObject(hdc, winBitmap)

    DI_NORMAL = 0x0003
    DrawIconEx(hdc, 0, 0, h_icon, w, h, 0, 0, DI_NORMAL)

    image = qt_fromWinHBITMAP(hdc, winBitmap, w, h)

    # NOTE: Not working: "ValueError: memoryview: invalid value for format 'B'" in `scanlineImage[x] |= 0xff000000`
    # from PySide.QtGui import qAlpha, qRed
    #
    # if not foundAlpha:
    #     for y in range(h):
    #         scanLine = image.scanLine(y)
    #
    #         for x in range(w):
    #             if qAlpha(scanLine[x]) != 0:
    #                 foundAlpha = True
    #                 break
    #
    # if not foundAlpha:
    #     # If no alpha was found, we use the mask to set alpha values
    #     DI_MASK = 0x0001
    #     DrawIconEx(hdc, 0, 0, h_icon, w, h, 0, 0, DI_MASK)
    #     mask = qt_fromWinHBITMAP(hdc, winBitmap, w, h)
    #
    #     for y in range(h):
    #         scanlineImage = image.scanLine(y)
    #         scanlineMask = 0 if mask.isNull() else mask.scanLine(y)
    #
    #         for x in range(w):
    #             if scanlineMask != 0 and qRed(scanlineMask[x]) != 0:
    #                 scanlineImage[x] = 0  # mask out this pixel
    #             else:
    #                 scanlineImage[x] |= 0xff000000  # set the alpha channel to 255

    # dispose resources created by iconinfo call
    DeleteObject(hbmMask.handle)
    DeleteObject(hbmColor.handle)

    # restore state
    SelectObject(hdc, oldhdc)
    DeleteObject(winBitmap)
    DeleteDC(hdc)

    return image


if __name__ == "__main__":
    h_icon = get_file_icon(r"C:\Users\ipetrash\Projects\alarm-clock\main.py")
    h_icon = get_file_icon(r"C:\Users\ipetrash\Desktop\Будильник.lnk")
    print("h_icon:", h_icon)

    QApplication([])

    px = fromWinHICON(h_icon)
    print(px, px.size())
    px.save("winapi_qt_get_icon_file_name.py.png")

    DestroyIcon(h_icon)
