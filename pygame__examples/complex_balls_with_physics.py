#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import math
import random

# SOURCE: http://archive.petercollingridge.co.uk/book/export/html/6
import pygame


background_colour = (255, 255, 255)
(width, height) = (400, 400)
mass_of_air = 0.2
elasticity = 0.75
gravity = (math.pi, 0.002)


def add_vectors(angle1, length1, angle2, length2) -> tuple[float, float]:
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2

    angle = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)

    return angle, length


def collide(p1, p2) -> None:
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        angle = math.atan2(dy, dx) + 0.5 * math.pi
        total_mass = p1.mass + p2.mass

        (p1.angle, p1.speed) = add_vectors(
            p1.angle,
            p1.speed * (p1.mass - p2.mass) / total_mass,
            angle,
            2 * p2.speed * p2.mass / total_mass,
        )
        (p2.angle, p2.speed) = add_vectors(
            p2.angle,
            p2.speed * (p2.mass - p1.mass) / total_mass,
            angle + math.pi,
            2 * p1.speed * p1.mass / total_mass,
        )
        p1.speed *= elasticity
        p2.speed *= elasticity

        overlap = 0.5 * (p1.size + p2.size - dist + 1)
        p1.x += math.sin(angle) * overlap
        p1.y -= math.cos(angle) * overlap
        p2.x -= math.sin(angle) * overlap
        p2.y += math.cos(angle) * overlap


class Particle:
    def __init__(self, x, y, size, mass=1) -> None:
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 0
        self.speed = 0
        self.angle = 0
        self.mass = mass
        self.drag = (self.mass / (self.mass + mass_of_air)) ** self.size

    def display(self) -> None:
        pygame.draw.circle(
            screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness
        )

    def move(self) -> None:
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag

    def bounce(self) -> None:
        if self.x > width - self.size:
            self.x = 2 * (width - self.size) - self.x
            self.angle = -self.angle
            self.speed *= elasticity

        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = -self.angle
            self.speed *= elasticity

        if self.y > height - self.size:
            self.y = 2 * (height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity


def find_particle(particles, x, y) -> Particle | None:
    for p in particles:
        if math.hypot(p.x - x, p.y - y) <= p.size:
            return p
    return None


def get_rand_color() -> tuple[int, int, int]:
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tutorial 9")

number_of_particles = 5
my_particles = []

for n in range(number_of_particles):
    size = random.randint(10, 20)
    density = random.randint(1, 20)
    x = random.randint(size, width - size)
    y = random.randint(size, height - size)

    particle = Particle(x, y, size, density * size**2)
    particle.colour = get_rand_color()
    particle.speed = random.random()
    particle.angle = random.uniform(0, math.pi * 2)

    my_particles.append(particle)

selected_particle = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            selected_particle = find_particle(my_particles, mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None

    if selected_particle:
        mouseX, mouseY = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.x
        dy = mouseY - selected_particle.y
        selected_particle.angle = 0.5 * math.pi + math.atan2(dy, dx)
        selected_particle.speed = math.hypot(dx, dy) * 0.1

    screen.fill(background_colour)

    for i, particle in enumerate(my_particles):
        particle.move()
        particle.bounce()
        for particle2 in my_particles[i + 1 :]:
            collide(particle, particle2)
        particle.display()

    pygame.display.flip()
    clock.tick(60)
