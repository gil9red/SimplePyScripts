#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import cv2
import pyautogui


class NotFoundItem(Exception):
    pass


def get_logger(name=__file__, file='log.txt', encoding='utf-8', dir_name='logs'):
    import os
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    file = dir_name + '/' + file

    import logging
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)d\t%(levelname)-8s %(message)s')

    # Simple file handler
    # fh = logging.FileHandler(file, encoding=encoding)
    # or:
    from logging.handlers import RotatingFileHandler
    fh = RotatingFileHandler(file, maxBytes=10000000, backupCount=5, encoding=encoding)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    import sys
    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setFormatter(formatter)
    log.addHandler(sh)

    return log


log = get_logger()


def crop_by_contour(img, contour):
    rect = cv2.boundingRect(contour)
    x, y, h, w = rect
    return img[y:y + h, x:x + w]


def get_game_board(img__or__file_name):
    if isinstance(img__or__file_name, str):
        img = cv2.imread(img__or__file_name)
    else:
        img = img__or__file_name

    # cv2.imshow('img', img)

    edges = cv2.Canny(img, 100, 200)
    # cv2.imshow('edges_img', edges)

    ret, thresh = cv2.threshold(edges, 200, 255, cv2.THRESH_BINARY)
    image, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow('image_', image)

    # cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
    # cv2.imshow('img_with_contour', img)
    #
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    if not contours:
        raise NotFoundItem('Не получилсоь найти контуры')

    log.info(
        'Всего контуров %s, поиск контура игрового поля: %s',
        len(contours), [cv2.contourArea(i) for i in contours if cv2.contourArea(i) > 10000]
    )

    contours = [i for i in contours if 249000 < cv2.contourArea(i) < 255000]
    if not contours:
        raise NotFoundItem('Не получилось найти контур поля игры')

    # img_with_contour = img.copy()
    # cv2.drawContours(img_with_contour, contours, -1, (0, 255, 0), 3)
    # cv2.imshow('img_with_contour', img_with_contour)

    crop_img = crop_by_contour(img, contours[-1])
    # cv2.imshow("cropped", crop_img)
    #
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    return crop_img


def get_cell_point_by_contour(board_img):
    # cv2.imshow("board_img", board_img)
    temp_board_img = board_img.copy()
    w, h, _ = temp_board_img.shape

    indent = 15
    size_cell = 122

    for i in range(5):
        cv2.rectangle(temp_board_img, (0, size_cell * i), (w, size_cell * i + indent), 0, cv2.FILLED)
        cv2.rectangle(temp_board_img, (size_cell * i, 0), (size_cell * i + indent, h), 0, cv2.FILLED)

    # cv2.imshow("temp_board_img", temp_board_img)

    gray_img = cv2.cvtColor(temp_board_img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray_img, 50, 255, cv2.THRESH_BINARY)
    gray_img_contours, cell_contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow("gray_img_contours", gray_img_contours)

    log.info('Контуров (%s): %s', len(cell_contours), [cv2.contourArea(i) for i in cell_contours])

    cell_contours = [i for i in cell_contours if cv2.contourArea(i) > 10000]
    log.info('Контуров ячеек: %s', len(cell_contours))

    if len(cell_contours) != 16:
        raise NotFoundItem('Нужно ровно 16 контуров ячеек')

    # img_with_contour = board_img.copy()
    # cv2.drawContours(img_with_contour, cell_contours, -1, (0, 255, 0), 3)
    # cv2.imshow('img_with_contour_' + str(hex(id(board_img))), img_with_contour)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    sort_x = sorted([cv2.boundingRect(x)[0] for x in cell_contours])
    mean_of_points = [
        sum(sort_x[0:4]) // 4,
        sum(sort_x[4:8]) // 4,
        sum(sort_x[8:12]) // 4,
        sum(sort_x[12:16]) // 4,
    ]

    # print(mean_of_points)
    MEAN_EPS = 5
    # print(sorted([cv2.boundingRect(x)[1] for x in cell_contours]))

    point_by_contour = dict()
    for contour in cell_contours:
        x, y, _, _ = cv2.boundingRect(contour)
        # print(x, y)

        for mean_point in mean_of_points:
            # Максимальное отклонение от средней позиции
            if abs(x - mean_point) <= MEAN_EPS:
                x = mean_point

            if abs(y - mean_point) <= MEAN_EPS:
                y = mean_point

        point_by_contour[(x, y)] = contour

    # cell_contours.sort(key=lambda x: (cv2.boundingRect(x)[1], cv2.boundingRect(x)[0]))
    # print([(cv2.boundingRect(contour)[0], cv2.boundingRect(contour)[1]) for contour in cell_contours])

    return point_by_contour


def show_cell_on_board(board_img, point_by_contour):
    image = board_img.copy()

    row = 0
    col = 0
    value_matrix = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]

    i = 1

    cell_contours = list(point_by_contour.values())

    # for contour in cell_contours:
    for pos, contour in sorted(point_by_contour.items(), key=lambda x: (x[0][1], x[0][0])):
        rect_cell = cv2.boundingRect(contour)
        x, y, w, h = rect_cell
        # x, y = pos

        cell_img = crop_by_contour(board_img, contour)
        main_color = get_main_color_bgr(cell_img)

        text_row_col = '{}x{}'.format(row, col)
        text_pos = '{}x{}'.format(x, y)
        print(text_row_col)
        print('   ', text_pos)

        cv2.putText(image, str(i), (x, y + h // 4), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0))
        cv2.putText(image, text_pos, (x + w // 3, y + h // 7), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 0))
        cv2.putText(image, text_row_col, (x + w // 8, y + int(h // 1.2)), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

        value_cell = get_value_by_color(main_color)
        print('    value:', value_cell)
        value_matrix[row][col] = value_cell

        if value_cell is not None:
            cv2.putText(image, str(value_cell), (x + w - 35, y + int(h // 1.2)), cv2.FONT_HERSHEY_PLAIN, 1.1,
                        (100, 100, 0))

        else:
            file_name = 'unknown_{}.png'.format('-'.join(map(str, main_color)))
            print('    NOT FOUND COLOR:', main_color, file_name)
            make_screenshot()
            cv2.imwrite(file_name, cell_img)

        col += 1
        if col == 4:
            col = 0
            row += 1

        i += 1

    print(value_matrix)

    cv2.drawContours(image, cell_contours, -1, (0, 255, 0), 3)
    cv2.imshow("img_with_contour_cell_contours_" + str(hex(id(image))), image)


def get_value_matrix_from_board(board_img):
    point_by_contour = get_cell_point_by_contour(board_img)

    # show_cell_on_board(board_img, point_by_contour)

    row = 0
    col = 0
    value_matrix = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]

    # for contour in cell_contours:
    for pos, contour in sorted(point_by_contour.items(), key=lambda x: (x[0][1], x[0][0])):
        cell_img = crop_by_contour(board_img, contour)
        main_color = get_main_color_bgr(cell_img)
        value_cell = get_value_by_color(main_color)
        log.debug('    value: %s', value_cell)
        value_matrix[row][col] = value_cell

        if value_cell is None:
            file_name = 'unknown_{}.png'.format('-'.join(map(str, main_color)))
            cv2.imwrite(file_name, cell_img)
            make_screenshot()
            raise NotFoundItem('NOT FOUND COLOR: {}, save in {}. Need update color in {}'.format(
                main_color, file_name, COLOR_BGR_BY_NUMBER
            ))

        col += 1
        if col == 4:
            col = 0
            row += 1

    log.debug('value_matrix: %s', value_matrix)
    return value_matrix


COLOR_BGR_BY_NUMBER = {
    (180, 192, 204): 0,  # None
    (217, 227, 237): 2,
    (199, 223, 235): 4,
    (122, 176, 241): 8,
    (98, 148, 244): 16,
    (94, 123, 244): 32,
    (59, 93, 246): 64,
    (115, 207, 236): 128,
    (98, 203, 236): 256,
    (82, 199, 236): 512,
    (65, 196, 235): 1024,
    (50, 193, 236): 2048,
    (50, 57, 60): 4096,
}


def get_value_by_color(color, deviation=5):
    def _generate_seq(value, deviation):
        """
        value = 5, deviation = 1 -> [4, 5, 6]
        value = 5, deviation = 2 -> [3, 4, 5, 6, 7]
        """

        left = list(range(value, value - deviation - 1, -1))
        right = list((range(value + 1, value + deviation + 1)))
        return list(sorted(left + right))

    for bgr_color, value in COLOR_BGR_BY_NUMBER.items():
        b1, g1, r1 = bgr_color
        b2, g2, r2 = color

        if b2 in _generate_seq(b1, deviation) \
                and g2 in _generate_seq(g1, deviation) \
                and r2 in _generate_seq(r1, deviation):
            return value

    return None


def get_main_color_bgr(image):
    img_points = []

    w, h = image.shape[:2]
    for i in range(h):
        for j in range(w):
            img_points.append(tuple(image[i, j]))

    from collections import Counter
    items = sorted(Counter(img_points).items(), reverse=True, key=lambda x: x[1])
    log.debug('Top 3 color: %s', items[:3])
    return items[0][0]


def get_next_move(value_matrix):
    # SOURCE: https://github.com/eshirazi/2048-bot
    from eshirazi_2048_bot.board import Board
    from eshirazi_2048_bot.board_score_heuristics import perfect_heuristic
    from eshirazi_2048_bot.board_score_strategy import ExpectimaxStrategy

    strategy = ExpectimaxStrategy(perfect_heuristic)

    board = Board(value_matrix)
    log.debug('board:\n%s', board)

    return str(strategy.get_next_move(board))


def locate_center_on_screen(needle_image, screenshot_image=None):
    if screenshot_image:
        rect = pyautogui.locate(needle_image, screenshot_image)
        if rect:
            return pyautogui.center(rect)

    return pyautogui.locateCenterOnScreen(needle_image)


def make_screenshot(prefix=''):
    pil_image = pyautogui.screenshot()

    from datetime import datetime
    file_name = datetime.now().strftime(prefix + '%d%m%y %H%M%S.jpg')
    log.info('Сохранение скриншота в ' + file_name)

    pil_image.save(file_name)

    return pil_image
