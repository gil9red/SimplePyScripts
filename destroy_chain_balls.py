#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def destroy_chain_balls(balls):
    # Будет работать с копией
    balls = list(balls)

    while balls:
        repeat_index_list = []
        last_ball = balls[0]

        for i in range(1, len(balls)):
            ball = balls[i]

            # Наткнулись на новый тип шарика
            if last_ball != ball:
                # Если не удалось набрать последовательность, чистим список
                if len(repeat_index_list) < 3:
                    repeat_index_list.clear()
                else:
                    # Последовательность есть, прерываем цикл
                    break

            repeat_index_list.append(i)
            last_ball = ball

        # Если перебор закончился, а последовательность не была найдена,
        # заканчиваем уничтожение шариков
        if len(repeat_index_list) < 3:
            break

        # Удаляем шарики из найденной последовательности
        for i in reversed(repeat_index_list):
            balls.pop(i)

        repeat_index_list.clear()

    return balls


if __name__ == "__main__":
    balls = [0, 1, 2, 3]
    balls_2 = destroy_chain_balls(balls)
    print(f"{balls} -> {balls_2}, уничтожено: {len(balls) - len(balls_2)}")

    balls = [0, 1, 2, 2, 1, 2, 3]
    balls_2 = destroy_chain_balls(balls)
    print(f"{balls} -> {balls_2}, уничтожено: {len(balls) - len(balls_2)}")

    balls = [0, 1, 2, 2, 1, 1, 1, 2, 3]
    balls_2 = destroy_chain_balls(balls)
    print(f"{balls} -> {balls_2}, уничтожено: {len(balls) - len(balls_2)}")

    balls = [1, 3, 3, 3, 2]
    balls_2 = destroy_chain_balls(balls)
    print(f"{balls} -> {balls_2}, уничтожено: {len(balls) - len(balls_2)}")

    balls = [1, 1, 1]
    balls_2 = destroy_chain_balls(balls)
    print(f"{balls} -> {balls_2}, уничтожено: {len(balls) - len(balls_2)}")

    balls = [1, 1]
    balls_2 = destroy_chain_balls(balls)
    print(f"{balls} -> {balls_2}, уничтожено: {len(balls) - len(balls_2)}")
