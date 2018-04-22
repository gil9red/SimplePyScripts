#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/llSourcell/deep_dream_challenge


# pip install tensorflow
import tensorflow as tf
import numpy as np
import PIL.Image
import matplotlib.pyplot as plt
import urllib.request
import os
import zipfile


# start with a gray image with a little noise
IMG_NOISE = np.random.uniform(size=(224, 224, 3)) + 100.0


# TODO: перенести сюда вспомогательные методы из основного скрипта
