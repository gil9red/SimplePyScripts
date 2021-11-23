#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time

import requests

from base_camera import BaseCamera
from config import PORT


URL_SCREENSHOT = f'http://127.0.0.1:{PORT}/command/SCREENSHOT'


class Camera(BaseCamera):
    @staticmethod
    def frames() -> bytes:
        while True:
            while True:
                try:
                    rs = requests.post(URL_SCREENSHOT)
                    break
                except:
                    time.sleep(0.5)

            yield rs.content

