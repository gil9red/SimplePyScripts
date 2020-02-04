#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import ctypes
import time


# SOURCE: https://stackoverflow.com/a/23468236/5909792


# SOURCE: https://gist.github.com/tracend/912308
# /****************************************************************************
#  *
#  *      DirectInput keyboard scan codes
#  *
#  ****************************************************************************/
DIK_ESCAPE = 0x01
DIK_1 = 0x02
DIK_2 = 0x03
DIK_3 = 0x04
DIK_4 = 0x05
DIK_5 = 0x06
DIK_6 = 0x07
DIK_7 = 0x08
DIK_8 = 0x09
DIK_9 = 0x0A
DIK_0 = 0x0B
DIK_MINUS = 0x0C  # - on main keyboard
DIK_EQUALS = 0x0D
DIK_BACK = 0x0E  # backspace
DIK_TAB = 0x0F
DIK_Q = 0x10
DIK_W = 0x11
DIK_E = 0x12
DIK_R = 0x13
DIK_T = 0x14
DIK_Y = 0x15
DIK_U = 0x16
DIK_I = 0x17
DIK_O = 0x18
DIK_P = 0x19
DIK_LBRACKET = 0x1A
DIK_RBRACKET = 0x1B
DIK_RETURN = 0x1C  # Enter on main keyboard
DIK_LCONTROL = 0x1D
DIK_A = 0x1E
DIK_S = 0x1F
DIK_D = 0x20
DIK_F = 0x21
DIK_G = 0x22
DIK_H = 0x23
DIK_J = 0x24
DIK_K = 0x25
DIK_L = 0x26
DIK_SEMICOLON = 0x27
DIK_APOSTROPHE = 0x28
DIK_GRAVE = 0x29  # accent grave
DIK_LSHIFT = 0x2A
DIK_BACKSLASH = 0x2B
DIK_Z = 0x2C
DIK_X = 0x2D
DIK_C = 0x2E
DIK_V = 0x2F
DIK_B = 0x30
DIK_N = 0x31
DIK_M = 0x32
DIK_COMMA = 0x33
DIK_PERIOD = 0x34  # . on main keyboard
DIK_SLASH = 0x35  # / on main keyboard
DIK_RSHIFT = 0x36
DIK_MULTIPLY = 0x37  # * on numeric keypad
DIK_LMENU = 0x38  # left Alt
DIK_SPACE = 0x39
DIK_CAPITAL = 0x3A
DIK_F1 = 0x3B
DIK_F2 = 0x3C
DIK_F3 = 0x3D
DIK_F4 = 0x3E
DIK_F5 = 0x3F
DIK_F6 = 0x40
DIK_F7 = 0x41
DIK_F8 = 0x42
DIK_F9 = 0x43
DIK_F10 = 0x44
DIK_NUMLOCK = 0x45
DIK_SCROLL = 0x46  # Scroll Lock
DIK_NUMPAD7 = 0x47
DIK_NUMPAD8 = 0x48
DIK_NUMPAD9 = 0x49
DIK_SUBTRACT = 0x4A  # - on numeric keypad
DIK_NUMPAD4 = 0x4B
DIK_NUMPAD5 = 0x4C
DIK_NUMPAD6 = 0x4D
DIK_ADD = 0x4E  # + on numeric keypad
DIK_NUMPAD1 = 0x4F
DIK_NUMPAD2 = 0x50
DIK_NUMPAD3 = 0x51
DIK_NUMPAD0 = 0x52
DIK_DECIMAL = 0x53  # . on numeric keypad
DIK_OEM_102 = 0x56  # <> or \| on RT 102-key keyboard (Non-U.S.)
DIK_F11 = 0x57
DIK_F12 = 0x58
DIK_F13 = 0x64  # = (NEC PC98)
DIK_F14 = 0x65  # = (NEC PC98)
DIK_F15 = 0x66  # = (NEC PC98)
DIK_KANA = 0x70  # (Japanese keyboard) =
DIK_ABNT_C1 = 0x73  # /? on Brazilian keyboard
DIK_CONVERT = 0x79  # (Japanese keyboard) =
DIK_NOCONVERT = 0x7B  # (Japanese keyboard) =
DIK_YEN = 0x7D  # (Japanese keyboard) =
DIK_ABNT_C2 = 0x7E  # Numpad . on Brazilian keyboard
DIK_NUMPADEQUALS = 0x8D  # = on numeric keypad (NEC PC98)
DIK_PREVTRACK = 0x90  # Previous Track (DIK_CIRCUMFLEX on Japanese keyboard)
DIK_AT = 0x91  # = (NEC PC98)
DIK_COLON = 0x92  # = (NEC PC98)
DIK_UNDERLINE = 0x93  # = (NEC PC98)
DIK_KANJI = 0x94  # (Japanese keyboard) =
DIK_STOP = 0x95  # = (NEC PC98)
DIK_AX = 0x96  # = (Japan AX)
DIK_UNLABELED = 0x97  # = (J3100)
DIK_NEXTTRACK = 0x99  # Next Track
DIK_NUMPADENTER = 0x9C  # Enter on numeric keypad
DIK_RCONTROL = 0x9D
DIK_MUTE = 0xA0  # Mute
DIK_CALCULATOR = 0xA1  # Calculator
DIK_PLAYPAUSE = 0xA2  # Play / Pause
DIK_MEDIASTOP = 0xA4  # Media Stop
DIK_VOLUMEDOWN = 0xAE  # Volume -
DIK_VOLUMEUP = 0xB0  # Volume +
DIK_WEBHOME = 0xB2  # Web home
DIK_NUMPADCOMMA = 0xB3  # , on numeric keypad (NEC PC98)
DIK_DIVIDE = 0xB5  # / on numeric keypad
DIK_SYSRQ = 0xB7
DIK_RMENU = 0xB8  # right Alt
DIK_PAUSE = 0xC5  # Pause
DIK_HOME = 0xC7  # Home on arrow keypad
DIK_UP = 0xC8  # UpArrow on arrow keypad
DIK_PRIOR = 0xC9  # PgUp on arrow keypad
DIK_LEFT = 0xCB  # LeftArrow on arrow keypad
DIK_RIGHT = 0xCD  # RightArrow on arrow keypad
DIK_END = 0xCF  # End on arrow keypad
DIK_DOWN = 0xD0  # DownArrow on arrow keypad
DIK_NEXT = 0xD1  # PgDn on arrow keypad
DIK_INSERT = 0xD2  # Insert on arrow keypad
DIK_DELETE = 0xD3  # Delete on arrow keypad
DIK_LWIN = 0xDB  # Left Windows key
DIK_RWIN = 0xDC  # Right Windows key
DIK_APPS = 0xDD  # AppMenu key
DIK_POWER = 0xDE  # System Power
DIK_SLEEP = 0xDF  # System Sleep
DIK_WAKE = 0xE3  # System Wake
DIK_WEBSEARCH = 0xE5  # Web Search
DIK_WEBFAVORITES = 0xE6  # Web Favorites
DIK_WEBREFRESH = 0xE7  # Web Refresh
DIK_WEBSTOP = 0xE8  # Web Stop
DIK_WEBFORWARD = 0xE9  # Web Forward
DIK_WEBBACK = 0xEA  # Web Back
DIK_MYCOMPUTER = 0xEB  # My Computer
DIK_MAIL = 0xEC  # Mail
DIK_MEDIASELECT = 0xED  # Media Select

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_UNICODE = 0x0004


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput
class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-hardwareinput
class HardwareInput(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_ushort)
    ]


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-mouseinput
class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]


class Input_I(ctypes.Union):
    _fields_ = [
        ("ki", KeyBdInput),
        ("mi", MouseInput),
        ("hi", HardwareInput)
    ]


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-input
class Input(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("ii", Input_I)
    ]


def press_key(hex_key_code: int):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hex_key_code, KEYEVENTF_SCANCODE, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_key(hex_key_code: int):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hex_key_code, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def write_key(hex_key_code: int, interval=0.1, pause=None):
    press_key(hex_key_code)
    time.sleep(interval)
    release_key(hex_key_code)

    if pause:
        time.sleep(pause)


if __name__ == '__main__':
    for i in [DIK_H, DIK_E, DIK_L, DIK_L, DIK_E, DIK_BACK, DIK_O]:
        write_key(i)
