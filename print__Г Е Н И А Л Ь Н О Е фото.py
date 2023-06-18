#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


text = "Г Е Н И А Л Ь Н О Е фото "
length = len(text)

for start in range(length + 1):
    new_text = ""
    for i in range(length):
        j = (start + i) % length
        new_text += text[j]

    if new_text[0] != " ":
        print(new_text)

# Г Е Н И А Л Ь Н О Е фото
# Е Н И А Л Ь Н О Е фото Г
# Н И А Л Ь Н О Е фото Г Е
# И А Л Ь Н О Е фото Г Е Н
# А Л Ь Н О Е фото Г Е Н И
# Л Ь Н О Е фото Г Е Н И А
# Ь Н О Е фото Г Е Н И А Л
# Н О Е фото Г Е Н И А Л Ь
# О Е фото Г Е Н И А Л Ь Н
# Е фото Г Е Н И А Л Ь Н О
# фото Г Е Н И А Л Ь Н О Е
# ото Г Е Н И А Л Ь Н О Е ф
# то Г Е Н И А Л Ь Н О Е фо
# о Г Е Н И А Л Ь Н О Е фот
# Г Е Н И А Л Ь Н О Е фото
