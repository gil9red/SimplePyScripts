#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path

# pip install opencv-python==4.13.0.92
import cv2


def crop_inner_game_screen(img: cv2.typing.MatLike) -> cv2.typing.MatLike | None:
    # 1. Переводим в оттенки серого
    gray: cv2.typing.MatLike = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Бинаризация (Threshold)
    # Все, что чернее, чем 10 (по шкале от 0 до 255), станет абсолютно черным (0).
    # Все, что ярче (сама игра и интерфейс Windows), станет абсолютно белым (255).
    _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

    # 3. Находим ВСЕ контуры на получившейся черно-белой маске
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    img_h, img_w = gray.shape
    total_area: int = img_h * img_w

    valid_boxes: list[tuple[int, tuple[int, int, int, int]]] = []
    for contour in contours:
        # Находим ограничивающий прямоугольник для каждого контура
        x, y, w, h = cv2.boundingRect(contour)
        area: int = w * h

        # Фильтруем контуры, чтобы отсечь мусор:
        # - Внутренний экран должен быть достаточно большим (например, больше 15% от всего скрина)
        # - Он не должен быть размером со весь экран (меньше 95%, чтобы отсечь сам скриншот)
        if (0.15 * total_area) < area < (0.95 * total_area):

            # Дополнительная проверка: проверяем, что внутри этого прямоугольника
            # нет синей полоски заголовка Windows (проверяем пропорции или координаты)
            # Окно игры на этом скрине находится ближе к центру, y явно больше 0.
            if (y > 10 and (y + h)) < (img_h - 10):
                # TODO: remove
                # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
                # cv2.rectangle(thresh, (x, y), (x + w, y + h), (0, 0, 255), 1)

                valid_boxes.append((area, (x, y, w, h)))

    # TODO: remove
    # dsize = 1280, 720
    # cv2.imshow("thresh", cv2.resize(thresh, dsize))
    # cv2.imshow("contours", cv2.resize(img, dsize))
    # # cv2.imshow("cropped", cv2.resize(cropped, dsize))
    # cv2.resizeWindow("contours", *dsize)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    if not valid_boxes:  # TODO:
        print("Внутренний экран игры не найден. Возможно, кадр слишком темный.")
        return None

    # Сортируем по площади. Нам нужен самый БОЛЬШОЙ прямоугольник,
    # который прошел фильтры и находится внутри черных полей.
    valid_boxes.sort(key=lambda item: item[0], reverse=True)
    _, (best_x, best_y, best_w, best_h) = valid_boxes[0]

    # 4. Вырезаем чистую игру
    cropped = img[best_y : best_y + best_h, best_x : best_x + best_w]

    print(
        f"Успешно вырезан внутренний экран: {best_w}x{best_h} в координатах x:{best_x}, y:{best_y}"
    )
    return cropped


# TODO:
PATH_DIR: Path = Path(r"C:\Users\ipetrash\Desktop\FF7 Screenshots\Карта Мира")
NAME_DIR_CROPPED: str = "cropped-game-screen"


for path in PATH_DIR.rglob("*.*"):
    if path.parent.name == NAME_DIR_CROPPED or path.suffix.lower() not in [
        ".png",
        ".jpg",
        ".jpeg",
    ]:
        continue

    path_img_cropped: Path = path.parent / NAME_DIR_CROPPED / path.name
    if path_img_cropped.exists():
        continue

    print()
    print(path)

    img: cv2.typing.MatLike | None = cv2.imread(path)
    if img is None:
        continue

    cropped: cv2.typing.MatLike | None = crop_inner_game_screen(img)
    if cropped is None:
        continue

    path_img_cropped.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(path_img_cropped, cropped)

    # TODO: remove
    # dsize = 1280, 720
    # cv2.imshow("original", cv2.resize(img, dsize))
    # cv2.imshow("cropped", cv2.resize(cropped, dsize))
    # cv2.resizeWindow("original", *dsize)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #
    # TODO: remove
    # dsize = 1280, 720
    # cv2.imshow("thresh", cv2.resize(thresh, dsize))
    # cv2.imshow("contours", cv2.resize(img, dsize))
    # # cv2.imshow("cropped", cv2.resize(cropped, dsize))
    # cv2.resizeWindow("contours", *dsize)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #
    # quit()

    print()
