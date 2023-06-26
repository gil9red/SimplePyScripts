#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/llSourcell/deep_dream_challenge


import io
import urllib.request
import os
import zipfile
from typing import Union


# pip install tensorflow
# import tensorflow as tf
import numpy as np
import PIL.Image
import matplotlib.pyplot as plt


# start with a gray image with a little noise
IMG_NOISE = np.random.uniform(size=(224, 224, 3)) + 100.0


# TODO: перенести сюда вспомогательные методы из основного скрипта


def download_tensorflow_model(data_dir='data/'):
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    url = 'https://storage.googleapis.com/download.tensorflow.org/models/inception5h.zip'
    model_name = os.path.split(url)[-1]

    local_zip_file = os.path.join(data_dir, model_name)
    if not os.path.exists(local_zip_file):
        print(f'Not found: {local_zip_file}. Step download...')

        # Download
        model_url = urllib.request.urlopen(url)
        with open(local_zip_file, 'wb') as output:
            output.write(model_url.read())

        print('Finish download. Step extract...')

        # Extract
        with zipfile.ZipFile(local_zip_file, 'r') as zip_ref:
            zip_ref.extractall(data_dir)

        print('Finish extract')


def showarray(a):
    a = np.uint8(np.clip(a, 0, 1) * 255)
    plt.imshow(a)
    plt.show()


def savearray(a, file_name: Union[io.BytesIO, str]):
    print('Saving to:', file_name)

    a = np.uint8(np.clip(a, 0, 1) * 255)
    PIL.Image.fromarray(a).save(file_name, format='jpeg')
