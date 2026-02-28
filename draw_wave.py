#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = "igrishaev"


"""Рисование волны wav-файла. Взято из http://habrahabr.ru/post/113239/"""


import math
import wave

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


types = {1: np.int8, 2: np.int16, 4: np.int32}


duration = nframes = k = peak = None


def format_time(x, pos=None):
    global duration, nframes, k
    progress = int(x / float(nframes) * duration * k)
    mins, secs = divmod(progress, 60)
    hours, mins = divmod(mins, 60)
    out = "%d:%02d" % (mins, secs)
    if hours > 0:
        out = "%d:" % hours
    return out


def format_db(x, pos=None):
    if pos == 0:
        return ""
    global peak
    if x == 0:
        return "-inf"

    db = 20 * math.log10(abs(x) / float(peak))
    return int(db)


def draw(file_name) -> None:
    wav = wave.open(file_name, mode="r")
    global nframes, k, peak, duration
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()

    duration = nframes / framerate
    w, h = 800, 300
    k = nframes / w / 32
    DPI = 72
    peak = 256**sampwidth / 2

    content = wav.readframes(nframes)
    samples = np.fromstring(content, dtype=types[sampwidth])

    plt.figure(1, figsize=(float(w) / DPI, float(h) / DPI), dpi=DPI)
    plt.subplots_adjust(wspace=0, hspace=0)

    for n in range(nchannels):
        channel = samples[n::nchannels]

        channel = channel[0::k]
        if nchannels == 1:
            channel = channel - peak

        axes = plt.subplot(2, 1, n + 1, axisbg="k")
        axes.plot(channel, "g")
        axes.yaxis.set_major_formatter(ticker.FuncFormatter(format_db))
        plt.grid(True, color="w")
        axes.xaxis.set_major_formatter(ticker.NullFormatter())

    axes.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
    # plt.savefig("wave", dpi=DPI)
    plt.show()
