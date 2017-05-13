#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: http://stackoverflow.com/questions/19749404/

import ctypes


# Define necessary structures
class XINPUT_VIBRATION(ctypes.Structure):
    _fields_ = [
        ("wLeftMotorSpeed", ctypes.c_ushort),
        ("wRightMotorSpeed", ctypes.c_ushort)
    ]

# Load Xinput.dll
xinput = ctypes.windll.xinput1_1

# Set up function argument types and return type
XInputSetState = xinput.XInputSetState
XInputSetState.argtypes = [ctypes.c_uint, ctypes.POINTER(XINPUT_VIBRATION)]
XInputSetState.restype = ctypes.c_uint


# You can also create a helper function like this:
def set_vibration(controller, left_motor, right_motor, duration=1.0):
    vibration = XINPUT_VIBRATION(int(left_motor * 65535), int(right_motor * 65535))

    import time
    t = time.time()

    while True:
        XInputSetState(controller, ctypes.byref(vibration))
        if time.time() - t >= duration:
            break

        time.sleep(0.1)


if __name__ == '__main__':
    set_vibration(0, 1.0, 0.5, duration=2.0)
