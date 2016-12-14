#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# def download_mp4_1280x720(url):
#     import pafy
#     video = pafy.new(url)
#
#     for s in video.videostreams:
#         if s.extension == 'mp4' and s.quality == '1280x720':
#             file_name = s.title + " " + s.quality + "." + s.extension
#             print(file_name, s.url)
#
#             s.download(file_name)
#
#             return file_name
#
#
# def extract_frames_from_video(file_name, save_to_dir):
#     """Функция сохраняет кадры из видео в указанную папку"""
#
#     import os
#     if not os.path.exists(save_to_dir):
#         os.mkdir(save_to_dir)
#
#     # -r = 0.1 = 1 / 10 т.е. по кадру через каждые 10 секунд
#     command_pattern = 'ffmpeg -i "{file_name}" -r {interval:.3f} -f image2 "{directory}/%09d.png"'
#     command = command_pattern.format(directory=save_to_dir, file_name=file_name, interval=1/60)
#
#     # ffmpeg -i "Горит от чатика - Dark Souls #1 1280x720.mp4" -r 0.017 -f image2 "extracted_images/%09d.jpg"
#     print(command)
#
#     from subprocess import Popen, DEVNULL
#     process = Popen(command, stderr=DEVNULL, stdout=DEVNULL)
#     print(process.wait())
#
#
# import time
#
#
# class Profiler:
#     def __enter__(self):
#         self._start_time = time.time()
#
#     def __exit__(self, type, value, traceback):
#         print("Elapsed time: {:.20f} sec".format(time.time() - self._start_time))
#
#
# with Profiler():
#     url = 'https://youtu.be/4ewTMva83tQ?list=PLndO6DOY2cLyxQYX7pkDspTJ42JWx07AO'
#     file_name = download_mp4_1280x720(url)
#     print(file_name)
#
#
# with Profiler():
#     extract_frames_from_video(file_name, 'png_extracted_images')
#
#
# quit()

import glob
import hashlib
from PIL import Image


BLACK_PXL = 0
WHITE_PXL = 255


def clear_img(im):
    im = im.copy()

    w, h = im.size
    for x in range(w):
        for y in range(h):
            pxl = im.getpixel((x, y))

            if pxl <= 170:
                im.putpixel((x, y), 0)
            else:
                im.putpixel((x, y), 255)

    return im


# file_name = 'extracted_images/000000159.jpg'
# im = Image.open(file_name).convert('L')
# im = im.crop(box=(1178, 5, 1255, 25))
# im.save('img.png')
#
# from collections import Counter
# print(im.histogram())
# print(Counter(im.histogram()))
#
# im = clear_img(im)
#
# print()
# print(im.histogram())
# print(Counter(im.histogram()))
#
# # import PIL.ImageOps
# # im = PIL.ImageOps.invert(im)
# im.save('img2.png')
#
#
# for file_name in [
#     '000000348.jpg',
#     '000000349.jpg',
#     '000000350.jpg',
#     '000000351.jpg',
#     '000000352.jpg'
# ]:
#     im = Image.open('extracted_images/' + file_name).convert('L')
#     im = im.crop(box=(1178, 5, 1255, 25))
#
#     im = clear_img(im)
#     print(im.histogram())
#     im.save(file_name)


# def get_hash_image(im):
#     hash = hashlib.new('md5')
#     hash.update(im.tobytes())
#     return hash.hexdigest()
#
#
# hash_by_images_dict = dict()
#
# for file_name in glob.glob('extracted_images/*.jpg'):
#     im = Image.open(file_name)
#     im = im.crop(box=(1178, 5, 1251, 25))
#
#     save_dir = 'crop_image_numbers'
#     import os
#     if not os.path.exists(save_dir):
#         os.mkdir(save_dir)
#
#     im.save(os.path.join(save_dir, os.path.basename(file_name)))
#
#     im = im.convert('L')
#     im = clear_img(im)
#
#     save_dir = 'crop_clear_image_numbers'
#     if not os.path.exists(save_dir):
#         os.mkdir(save_dir)
#
#     # Фильтр одноцветных изображений -- они полностью белые или черные
#     from collections import Counter
#     if len(Counter(im.histogram())) == 2:
#         continue
#
#     im.save(os.path.join(save_dir, os.path.basename(file_name)))
#
#     im_hash = get_hash_image(im)
#     hash_by_images_dict[im_hash] = im
#
# print(len(hash_by_images_dict))
#
# save_dir = 'hash_crop_image_numbers'
# import os
# if not os.path.exists(save_dir):
#     os.mkdir(save_dir)
#
# for hash_im, im in hash_by_images_dict.items():
#     im.save(os.path.join(save_dir, hash_im + '.jpg'))
