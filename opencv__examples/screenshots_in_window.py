#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.stackoverflow.com/questions/926556/


import threading

import cv2
import numpy as np

from PIL import ImageGrab


target_array = None


def go():
    global target_array
    while True:
        if target_array is not None:
            cv2.imshow("hello", target_array)
            k = cv2.waitKey(5) & 0xFF

            # <Escape>
            if k == 27:
                break


if __name__ == "__main__":
    thread = threading.Thread(target=go)
    thread.start()

    while True:
        img = ImageGrab.grab(bbox=(0, 0, 300, 300))
        target_array = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    cv2.destroyAllWindows()
