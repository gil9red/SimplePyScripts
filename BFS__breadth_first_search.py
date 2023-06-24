#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"

# SOURCE: https://stackoverflow.com/a/47902476/5909792


from collections import deque
from typing import Any


# Breadth-first search
def bfs(
    grid: list[list[Any]], start: tuple[Any, Any], goal: Any, wall: Any
) -> list[tuple[Any, Any]]:
    width, height = len(grid[0]), len(grid)
    queue = deque([[start]])
    seen = {start}

    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if grid[y][x] == goal:
            return path

        for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if (
                0 <= x2 < width
                and 0 <= y2 < height
                and grid[y2][x2] != wall
                and (x2, y2) not in seen
            ):
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))


if __name__ == "__main__":
    start = 5, 2
    wall, goal = "#", "*"
    grid = [
        list(".........."),
        list("..*#...##."),
        list("..##...#*."),
        list(".....###.."),
        list("......*..."),
    ]
    x, y = start
    grid[y][x] = "@"  # Start
    print("\n".join("".join(row) for row in grid))
    # ..........
    # ..*#...##.
    # ..##.@.#*.
    # .....###..
    # ......*...

    print()

    path = bfs(grid, start, goal, wall)
    print(path)
    # [(5, 2), (4, 2), (4, 3), (4, 4), (5, 4), (6, 4)]

    for x, y in path[1:]:
        grid[y][x] = "x"
    print("\n".join("".join(row) for row in grid))
    # ..........
    # ..*#...##.
    # ..##x@.#*.
    # ....x###..
    # ....xxx...
