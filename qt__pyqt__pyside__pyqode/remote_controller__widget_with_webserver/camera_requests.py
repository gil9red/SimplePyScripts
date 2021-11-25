#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time

import requests

from base_camera import BaseCamera
from config import PORT


URL_SCREENSHOT = f'http://127.0.0.1:{PORT}/command/SCREENSHOT'


class Camera(BaseCamera):
    FPS = 30
    IS_PRINTING_FPS = False

    @staticmethod
    def frames() -> bytes:
        frame_period = 1.0 / Camera.FPS
        now = time.time()
        next_frame = now + frame_period

        start_time = time.time()
        counter = 0

        while True:
            rs = requests.post(URL_SCREENSHOT)
            yield rs.content

            # Ограничение работы по FPS
            while now < next_frame:
                time.sleep(next_frame - now)
                now = time.time()
            next_frame += frame_period

            if Camera.IS_PRINTING_FPS:
                counter += 1
                if (time.time() - start_time) >= 1:
                    fps = counter / (time.time() - start_time)
                    print(f"FPS: {fps:.2f}")
                    counter = 0
                    start_time = time.time()
