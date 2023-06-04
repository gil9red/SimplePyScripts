#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/qbittorrent/qBittorrent/blob/ccd8f3e0f1447c0f88fedb975b52e2691722d6e9/src/base/bittorrent/torrenthandle.cpp#L302


from glob import glob, escape as glob_escape
from os.path import join, normpath, getsize, isfile
from os import listdir

from common import get_client, sizeof_fmt


qb = get_client()

save_path_current_paths = []

for save_path in set(torrent["save_path"] for torrent in qb.torrents()):
    for file_name in listdir(save_path):
        if file_name == ".unwanted":
            continue

        path = normpath(join(save_path, file_name))
        save_path_current_paths.append(path)


torrent_content_path_list = []


for torrent in qb.torrents(sort="name"):
    # Нужны только те торренты, что скачаны (хоть частично)
    if torrent["downloaded"] == 0:
        continue

    files = qb.get_torrent_files(torrent["hash"])

    save_path = torrent["save_path"]
    first_file_path = files[0]["name"]

    # Найдем первый разделите папки
    index = first_file_path.find("/")
    if index == -1:
        index = first_file_path.find("\\")

    if index != -1:
        # Путь до папки торрента
        torrent_content_path = join(save_path, first_file_path[:index])
    else:
        # Путь до файла торрента (когда торрент состоит из одного файла)
        torrent_content_path = join(save_path, first_file_path)

    torrent_content_path = normpath(torrent_content_path)

    torrent_content_path_list.append(torrent_content_path)


# Получим файлы, что есть в <save_path_current_paths>, но нет в torrent_content_path_list
items = sorted(set(save_path_current_paths) - set(torrent_content_path_list))
print(len(items), items)

total_size = 0

for path in items:
    if isfile(path):
        size = getsize(path)
    else:
        # Найдем все файлы в папке и подпапках и подсчитаем их суммарный размер
        sub_files = filter(isfile, glob(glob_escape(path) + "/**", recursive=True))
        size = sum(getsize(file_name) for file_name in sub_files)

    total_size += size
    print(f"{path} ({size} / {sizeof_fmt(size)})")

print()

print(f"Total size: {total_size} / {sizeof_fmt(total_size)}")
