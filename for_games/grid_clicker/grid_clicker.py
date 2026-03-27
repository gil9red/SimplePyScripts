#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import argparse
import threading
import time
import sys

# pip install pyautogui==0.9.54
import pyautogui

# pip install pynput==1.8.1
from pynput import mouse

# pip install screeninfo==0.8.1
from screeninfo import Monitor, get_monitors


pyautogui.FAILSAFE = False

# Глобальный флаг работы
is_running = True


def on_click(x, y, button, pressed) -> bool | None:
    global is_running
    # Если нажата правая кнопка мыши (любая: нажатие или отпускание)
    if button == mouse.Button.right:
        print("\n[!] Обнаружен клик правой кнопкой. Останавливаю...")
        is_running = False
        return False  # Останавливает сам слушатель pynput


def start_click_listener() -> None:
    # Запуск прослушивания мыши в отдельном потоке
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


def click_all_on_screen(
    step: int = 50,
    do_click: bool = False,
    # Режим 1: Прямые координаты
    coords: tuple[int, int, int, int] | None = None,  # (x1, y1, x2, y2)
    # Режим 2: По номеру монитора
    monitor_number: int = 1,
    sleep_time_between_clicks_ms: int = 10,
    offset_top: int = 50,  # Защитный отступ сверху
    offset_bottom: int = 50,  # Защитный отступ снизу
    offset_left: int = 50,  # Защитный отступ слева
    offset_right: int = 50,  # Защитный отступ справа
) -> None:
    global is_running

    if not do_click:
        print("[!] ВНИМАНИЕ: Режим имитации включен, клики производиться не будут.")

    # Запуск потока для-прерывателя
    threading.Thread(target=start_click_listener, daemon=True).start()

    # Режим 1: Прямые координаты
    if coords:
        start_x, start_y, end_x, end_y = coords
        print(f"Режим ручных координат: X({start_x}..{end_x}), Y({start_y}..{end_y})")

    # Режим 2: По номеру монитора
    else:
        monitors = get_monitors()
        try:
            monitor: Monitor = monitors[monitor_number - 1]
        except IndexError:
            print(f"[#] Ошибка: Номер монитора должен быть от 1 до {len(monitors)}")
            return

        # Определяем границы с учетом отступов
        start_x = monitor.x + offset_left
        end_x = monitor.x + monitor.width - offset_right
        start_y = monitor.y + offset_top
        end_y = monitor.y + monitor.height - offset_bottom
        print(f"Режим монитора #{monitor_number} с отступами.")

    print(f"Область: X от {start_x} до {end_x}, Y от {start_y} до {end_y}")
    print(f"Шаг: {step}px")

    sleep_time_between_clicks_secs: float = sleep_time_between_clicks_ms / 1000

    time.sleep(3)

    print("Работаю. Нажми ПРАВУЮ кнопку мыши для стопа.")

    for y in range(start_y, end_y, step):
        for x in range(start_x, end_x, step):
            if not is_running:
                print("Программа экстренно завершена.")
                return

            pyautogui.moveTo(x, y)
            if do_click:
                pyautogui.click(x, y)
            time.sleep(sleep_time_between_clicks_secs)

    print("Готово!")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="GridClicker: Скрипт для протыкивания экрана по сетке.",
        # Этот параметр автоматически добавит (default: ...) в описание каждого аргумента
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    base_group = parser.add_argument_group("Основные настройки")
    base_group.add_argument("-s", "--step", type=int, default=50, help="Шаг сетки")
    base_group.add_argument(
        "--do-click",
        action="store_true",
        help="РАЗРЕШИТЬ клики (без этого флага только перемещение курсора)",
    )
    base_group.add_argument(
        "-t",
        "--sleep",
        type=int,
        default=10,
        dest="sleep_time_between_clicks_ms",
        help="Задержка (мс)",
    )

    # Новая группа для координат
    coord_group = parser.add_argument_group(
        "Режим конкретных координат (игнорирует настройки монитора)"
    )
    coord_group.add_argument("--x1", type=int, help="Левая граница")
    coord_group.add_argument("--y1", type=int, help="Верхняя граница")
    coord_group.add_argument("--x2", type=int, help="Правая граница")
    coord_group.add_argument("--y2", type=int, help="Нижняя граница")

    monitor_group = parser.add_argument_group(
        "Настройки монитора (используются, если не заданы x1,y1,x2,y2)"
    )
    monitor_group.add_argument(
        "-m", "--monitor", type=int, default=1, dest="monitor_number"
    )
    monitor_group.add_argument("--top", type=int, default=50, dest="offset_top")
    monitor_group.add_argument("--bottom", type=int, default=50, dest="offset_bottom")
    monitor_group.add_argument("--left", type=int, default=50, dest="offset_left")
    monitor_group.add_argument("--right", type=int, default=50, dest="offset_right")

    args = parser.parse_args()

    # Если скрипт запущен без аргументов — показываем help и выходим
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    # Собираем координаты в кортеж, если они все указаны
    coords: tuple[int, int, int, int] | None = None
    if all(v is not None for v in [args.x1, args.y1, args.x2, args.y2]):
        coords = args.x1, args.y1, args.x2, args.y2

    click_all_on_screen(
        step=args.step,
        do_click=args.do_click,
        coords=coords,
        monitor_number=args.monitor_number,
        sleep_time_between_clicks_ms=args.sleep_time_between_clicks_ms,
        offset_top=args.offset_top,
        offset_bottom=args.offset_bottom,
        offset_left=args.offset_left,
        offset_right=args.offset_right,
    )


if __name__ == "__main__":
    # NOTE: Пример использования, режим прямых координат
    # NOTE: grid_clicker.py --x1=-545 --y1=322 --x2=-42 --y2=1073
    # NOTE: grid_clicker.py --do-click --x1=-545 --y1=322 --x2=-42 --y2=1073
    # click_all_on_screen(
    #     step=100,
    #     coords=(-545, 322, -42, 1073),
    # )

    # NOTE: Пример использования, режим монитора
    # click_all_on_screen(
    #     step=100,
    #     monitor_number=2,
    #     # sleep_time_between_clicks_ms=0.005, # 5 мс
    #     offset_bottom=150,
    # )

    main()
