#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "ipetrash"


# https://mail.python.org/pipermail/python-win32/2007-June/006174.html


import copy
import ctypes
import sys

import win32con


TH32CS_SNAPPROCESS = 0x00000002


class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", ctypes.c_ulong),
        ("cntUsage", ctypes.c_ulong),
        ("th32ProcessID", ctypes.c_ulong),
        ("th32DefaultHeapID", ctypes.c_ulong),
        ("th32ModuleID", ctypes.c_ulong),
        ("cntThreads", ctypes.c_ulong),
        ("th32ParentProcessID", ctypes.c_ulong),
        ("pcPriClassBase", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("szExeFile", ctypes.c_char * 260),
    ]

    def __str__(self) -> str:
        return (
            "szExeFile={} "
            "th32ProcessID={} "
            "cntThreads={} "
            "cntUsage={} "
            "dwFlags={} "
            "dwSize={} "
            "pcPriClassBase={} "
            "th32DefaultHeapID={} "
            "th32ModuleID={} "
            "th32ParentProcessID={} "
            "".format(
                self.szExeFile,
                self.th32ProcessID,
                self.cntThreads,
                self.cntUsage,
                self.dwFlags,
                self.dwSize,
                self.pcPriClassBase,
                self.th32DefaultHeapID,
                self.th32ModuleID,
                self.th32ParentProcessID,
            )
        )


def process_list():
    # See http://msdn2.microsoft.com/en-us/library/ms686701.aspx
    CreateToolhelp32Snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot
    Process32First = ctypes.windll.kernel32.Process32First
    Process32Next = ctypes.windll.kernel32.Process32Next
    CloseHandle = ctypes.windll.kernel32.CloseHandle
    hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)

    pe32 = PROCESSENTRY32()
    pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)
    if Process32First(hProcessSnap, ctypes.byref(pe32)) == win32con.FALSE:
        print("Failed getting first process.", file=sys.stderr)
        return

    while True:
        yield copy.deepcopy(pe32)

        if Process32Next(hProcessSnap, ctypes.byref(pe32)) == win32con.FALSE:
            break

    CloseHandle(hProcessSnap)


# for process in process_list():
#     print(process)
#
for process in sorted(process_list(), key=lambda x: x.szExeFile):
    print(process)

# for process in sorted(process_list(), key=lambda x: x.th32ProcessID):
#     print(process)
