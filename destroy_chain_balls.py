#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def destroy_chain_balls(balls):
    # Будет работать с копией
    balls = list(balls)

    while True:
        repeat_index = [0]
        last_ball = balls[0]

        for i in range(1, len(balls)):
            ball = balls[i]

            if last_ball != ball:
                if len(repeat_index) < 3:
                    repeat_index.clear()
                else:
                    break

            repeat_index.append(i)
            last_ball = ball

        if len(repeat_index) < 3:
            break

        for i in reversed(repeat_index):
            balls.pop(i)

        repeat_index.clear()

    return balls


if __name__ == '__main__':
    balls = [0, 1, 2, 3]
    balls_2 = destroy_chain_balls(balls)
    print("{} -> {}, уничтожено: {}".format(balls, balls_2, len(balls) - len(balls_2)))

    balls = [0, 1, 2, 2, 1, 2, 3]
    balls_2 = destroy_chain_balls(balls)
    print("{} -> {}, уничтожено: {}".format(balls, balls_2, len(balls) - len(balls_2)))

    balls = [0, 1, 2, 2, 1, 1, 1, 2, 3]
    balls_2 = destroy_chain_balls(balls)
    print("{} -> {}, уничтожено: {}".format(balls, balls_2, len(balls) - len(balls_2)))

    balls = [1, 3, 3, 3, 2]
    balls_2 = destroy_chain_balls(balls)
    print("{} -> {}, уничтожено: {}".format(balls, balls_2, len(balls) - len(balls_2)))
