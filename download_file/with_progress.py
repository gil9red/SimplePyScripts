#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from urllib.request import urlretrieve
from threading import Thread


def reporthook(blocknum, blocksize, totalsize) -> None:
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 100.0 / totalsize
        if percent > 100:
            percent = 100
            readsofar = totalsize

        s = "\r%5.1f%% %*d / %d" % (percent, len(str(totalsize)), readsofar, totalsize)
        sys.stdout.write(s)
        if readsofar >= totalsize:  # Near the end
            sys.stdout.write("\n")

    # Total size is unknown
    else:
        sys.stdout.write(f"read {readsofar}\n")


def download(
    url: str, file_name: str = None, as_thread=False, callback_func=None
) -> str:
    if as_thread:

        def run(url, file_name, reporthook, callback_func):
            local_file_name, _ = urlretrieve(url, file_name, reporthook=reporthook)
            if callable(callback_func):
                callback_func(local_file_name)
            return local_file_name

        thread = Thread(target=run, args=(url, file_name, reporthook, callback_func))
        thread.start()

    else:
        return urlretrieve(url, file_name, reporthook=reporthook)[0]


if __name__ == "__main__":
    URL = "https://codeload.github.com/gil9red/SimplePyScripts/zip/master"
    print(download(URL))
    print()
    print(download(URL, "SimplePyScripts.zip"))

    print("\n")
    sys.stderr.write("Threading...\n")

    print(download(URL, "SimplePyScripts.zip", as_thread=True))

    def callback_func(file_name: str) -> None:
        print("File name:", file_name)

    print(
        download(
            URL, "SimplePyScripts.zip", as_thread=True, callback_func=callback_func
        )
    )
