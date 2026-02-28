#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# https://msdn.microsoft.com/en-us/library/aa373208(VS.85).aspx


import ctypes


ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_AWAYMODE_REQUIRED = 0x00000040
ES_DISPLAY_REQUIRED = 0x00000002

SetThreadExecutionState = ctypes.windll.kernel32.SetThreadExecutionState


def preventing_on() -> None:
    # Television recording is beginning. Enable away mode and prevent the sleep idle time-out.
    SetThreadExecutionState(
        ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_AWAYMODE_REQUIRED | ES_DISPLAY_REQUIRED
    )


def preventing_off() -> None:
    # Clear EXECUTION_STATE flags to disable away mode and allow the system to idle to sleep normally.
    SetThreadExecutionState(ES_CONTINUOUS)


if __name__ == "__main__":
    import time

    preventing_on()

    # Wait 1 hours
    time.sleep(60 * 60)

    # # infinity
    # while True:
    #     time.sleep(1)

    preventing_off()
