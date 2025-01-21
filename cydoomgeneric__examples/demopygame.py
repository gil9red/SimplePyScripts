"""
 Copyright(C) 2024 Wojciech Graj
 Copyright(C) 2024 Miika Lönnqvist

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2
 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
"""

import sys
from typing import Optional

import numpy as np
import pygame

import cydoomgeneric as cdg

keymap = {
    pygame.K_LEFT: cdg.Keys.LEFTARROW,
    pygame.K_RIGHT: cdg.Keys.RIGHTARROW,
    pygame.K_UP: cdg.Keys.UPARROW,
    pygame.K_DOWN: cdg.Keys.DOWNARROW,
    pygame.K_COMMA: cdg.Keys.STRAFE_L,
    pygame.K_PERIOD: cdg.Keys.STRAFE_R,
    pygame.K_LCTRL: cdg.Keys.FIRE,
    pygame.K_SPACE: cdg.Keys.USE,
    pygame.K_RSHIFT: cdg.Keys.RSHIFT,
    pygame.K_RETURN: cdg.Keys.ENTER,
    pygame.K_ESCAPE: cdg.Keys.ESCAPE,
}


class PygameDoom:

    def __init__(self) -> None:
        self._resx = 640
        self._resy = 400
        pygame.init()
        self._screen = pygame.display.set_mode((self._resx, self._resy))

    def draw_frame(self, pixels: np.ndarray) -> None:
        pixels = np.rot90(pixels)
        pixels = np.flipud(pixels)
        pygame.surfarray.blit_array(self._screen, pixels[:, :, [2, 1, 0]])
        pygame.display.flip()

    def get_key(self) -> Optional[tuple[int, int]]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in keymap:
                    return 1, keymap[event.key]

            if event.type == pygame.KEYUP:
                if event.key in keymap:
                    return 0, keymap[event.key]

        return None

    def set_window_title(self, t: str) -> None:
        pygame.display.set_caption(t)


if __name__ == "__main__":
    g = PygameDoom()
    cdg.init(g._resx,
             g._resy,
             g.draw_frame,
             g.get_key,
             set_window_title=g.set_window_title)
    cdg.main()
