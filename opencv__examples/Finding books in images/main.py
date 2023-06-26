#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://tproger.ru/translations/finding-books-python-opencv/


# pip install opencv-python
import cv2


# Загрузка изображения
image = cv2.imread("example.jpg")
# cv2.imshow('image', image)

# Черно-белое изображение
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Размытие
gray = cv2.GaussianBlur(gray, (3, 3), 0)
# cv2.imshow('gray', gray)

# Распознавание контуров
edged = cv2.Canny(gray, 10, 250)
# cv2.imshow('edged', edged)

# Закрытие открытых контуров
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
# cv2.imshow('closed', closed)

# Нахождение контуров в изображении и подсчет количества книг
contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
total = 0

image_result = image.copy()

# Сортировка по X. Нужна только для того, чтобы слева направо пронумеровать найденных книги
contours = sorted(contours, key=lambda c: cv2.boundingRect(c[0]))

# Перебор контуров
for c in contours:
    # Аппроксимирование (сглаживание) контура
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    # Если у контура 4 вершины, предполагаем, что это книга
    if len(approx) != 4:
        continue

    cv2.drawContours(image_result, [approx], -1, (0, 255, 0), 4)
    total += 1

    # Получение центра контура
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    cv2.putText(
        image_result,
        str(total),
        (cX, cY),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.5,
        (0, 255, 0),
        2,
    )

print(f"На картинке {total} книг(и)")
cv2.imwrite("output.jpg", image_result)
cv2.imshow("image_result", image_result)

cv2.waitKey()
