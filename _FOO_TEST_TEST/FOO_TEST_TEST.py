#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from random import randint

# pip install pygame
import pygame


class Ball:
    def __init__(self, x, y, r, v_x, v_y, color):
        self.x = x
        self.y = y
        self.r = r
        self.v_x = v_x
        self.v_y = v_y
        self.color = color

    def update(self):
        self.x += self.v_x
        self.y += self.v_y

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.center, self.r)

        # Нарисуем поверх первого, прозрачный второй с границей (параметр width)
        pygame.draw.circle(surface, (0, 0, 0), self.center, self.r, 1)

    @property
    def center(self):
        return self.x, self.y

    @property
    def top(self):
        return self.y - self.r

    @property
    def bottom(self):
        return self.y + self.r

    @property
    def left(self):
        return self.x - self.r

    @property
    def right(self):
        return self.x + self.r


FPS = 60
WIDTH = 600  # ширина экрана
HEIGHT = 600  # высота экрана
BACKGROUND_COLOR = (255, 255, 255)
BALL_NUMBER = 100

pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def create_random_ball(width, height) -> Ball:
    def get_random_vector():
        pos = 0, 0
        # Если pos равен (0, 0), пересчитываем значения, т.к. шарик должен двигаться
        while pos == (0, 0):
            pos = randint(-3, 3), randint(-3, 3)

        return pos

    def get_random_color():
        return randint(0, 255), randint(0, 255), randint(0, 255)
    
    x = width // 2 + randint(-width // 4, width // 4)
    y = height // 2 + randint(-height // 4, height // 4)
    r = randint(10, 20)
    v_x, v_y = get_random_vector()
    color = get_random_color()

    return Ball(x, y, r, v_x, v_y, color)


balls = [create_random_ball(WIDTH, HEIGHT) for _ in range(BALL_NUMBER)]

game_active = True

while True:
    for event in pygame.event.get():  # получение всех событий
        if event.type == pygame.QUIT:  # проверка события "Выход"
            game_active = False
            break

    is_pressed = pygame.key.get_pressed()
    if is_pressed[pygame.K_ESCAPE]:
        game_active = False

    if not game_active:
        break

    surface.fill(BACKGROUND_COLOR)

    for ball in balls:
        ball.draw(surface)
        ball.update()

        # Условия отскакивания шарика от левого и правого края
        if ball.left <= 0 or ball.right >= WIDTH:
            ball.v_x = -ball.v_x

        # Условия отскакивания шарика верхнего и нижнего края
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball.v_y = -ball.v_y

    pygame.display.set_caption("[{} fps]".format(int(clock.get_fps())))
    pygame.display.update()

    clock.tick(FPS)
    pygame.event.pump()
