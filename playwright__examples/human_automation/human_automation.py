#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import random
import re
import string

from typing import Callable, TypedDict

# playwright>=1.61.0
from playwright.sync_api import Page, Locator, TimeoutError

# playwright-stealth>=2.0.3
from playwright_stealth import Stealth

# python-ghost-cursor==0.1.1
from python_ghost_cursor.playwright_sync import create_cursor
from python_ghost_cursor.playwright_sync._spoof import GhostCursor

type Point = TypedDict("Point", {"x": int, "y": int})


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

stealth = Stealth()


def get_center_page(page: Page) -> Point:
    # Get the size of the current browser window
    viewport: dict[str, int] | None = page.viewport_size

    base_x: int
    base_y: int
    if viewport:
        base_x = viewport["width"] // 2
        base_y = viewport["height"] // 2
    else:
        base_x, base_y = 640, 360

    offset_x: int = random.randint(-40, 40)
    offset_y: int = random.randint(-40, 40)

    target_x: int = base_x + offset_x
    target_y: int = base_y + offset_y

    return {"x": target_x, "y": target_y}


def inject_cursor(page: Page) -> None:
    page.add_init_script("""
        (() => {
            const initCursor = () => {
                const box = document.createElement('div');
                box.id = 'playwright-fake-cursor';
                box.style.position = 'fixed';
                box.style.top = '0';
                box.style.left = '0';
                box.style.width = '14px';
                box.style.height = '14px';
                box.style.background = 'rgba(255, 0, 0, 0.7)';
                box.style.border = '2px solid white';
                box.style.borderRadius = '50%';
                box.style.pointerEvents = 'none';
                box.style.zIndex = '999999';
                box.style.transform = 'translate(-50%, -50%)';
                document.body.appendChild(box);
    
                document.addEventListener('mousemove', (e) => {
                    box.style.left = e.clientX + 'px';
                    box.style.top = e.clientY + 'px';
                });
            };
            
            // If the DOM has already been loaded (unlikely for init_script, but useful for safety)
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', initCursor);
            } else {
                initCursor();
            }
        })();
    """)


TYPO_CHAR_SETS: dict[str, str] = {
    "eng_lower": string.ascii_lowercase,
    "eng_upper": string.ascii_uppercase,
    "rus_lower": "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
    "rus_upper": "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
    "digits": string.digits,
    "punctuation": string.punctuation,
}

WAIT_MS: tuple[int, int] = 100, 250


class HumanAutomation:
    page: Page
    cursor: GhostCursor
    typo_char_sets: dict[str, str]

    def __init__(
        self,
        page: Page,
        typo_char_sets: dict[str, str] | None = None,
    ) -> None:
        if typo_char_sets is None:
            typo_char_sets = TYPO_CHAR_SETS

        self.page = page
        self.cursor = create_cursor(page, start=get_center_page(page))
        self.typo_char_sets = typo_char_sets

        stealth.apply_stealth_sync(page)
        inject_cursor(page)

    def wait(self, min_time_ms: int, max_time_ms: int) -> None:
        self.page.wait_for_timeout(random.randint(min_time_ms, max_time_ms))

    def move_to(
        self,
        locator: Locator | str,
        wait_ms: tuple[int, int] = WAIT_MS,
    ) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        log.info(f"Moving to: {locator}")

        self.scroll_to_element(locator)

        self.cursor.move(locator)
        self.wait(*wait_ms)

    def click(
        self,
        locator: Locator | str,
        wait_ms: tuple[int, int] = WAIT_MS,
    ) -> None:
        if isinstance(locator, str):
            locator = self.page.locator(locator)

        log.info(f"Clicking to: {locator}")

        # NOTE: move_to is not suitable here - the cursor moves twice
        #       It internally calls cursor.move, which moves the cursor
        #       click internally calls cursor.click, which also calls cursor.move
        self.scroll_to_element(locator)

        # NOTE: If this is a link, removing the 'target' attribute will prevent opening in a new tab
        locator.evaluate("el => el.removeAttribute('target')")

        self.cursor.click(locator)
        self.wait(*wait_ms)

    def scroll_to_element(
        self,
        locator: Locator | str,
        margin: int = 100,
        wait_ms: tuple[int, int] = WAIT_MS,
    ) -> None:
        """
        Simulates human scrolling.
        If the element is fully visible on the screen, no scrolling occurs.
        If the element is hidden (at the top or bottom), it will smoothly scroll closer to the center.
        """

        if isinstance(locator, str):
            locator = self.page.locator(locator)

        log.info(f"Scrolling to: {locator}")

        while True:
            box: dict[str, float] | None
            try:
                box = locator.bounding_box(timeout=100)
            except TimeoutError:
                box = None

            if not box:
                # If the element is not in the DOM at all, scroll down randomly
                self.page.mouse.wheel(0, random.randint(250, 450))
                self.wait(*wait_ms)
                continue

            viewport_height = self.page.viewport_size["height"]

            # Find the boundaries of the element relative to the screen
            element_top = box["y"]
            element_height = box["height"]
            element_bottom = element_top + element_height

            is_top_visible = element_top >= margin
            is_bottom_within_viewport = element_bottom <= (viewport_height - margin)
            is_too_large = element_height > (viewport_height - (margin * 2))
            is_bottom_visible = is_bottom_within_viewport or is_too_large
            if is_top_visible and is_bottom_visible:  # The element is perfectly visible
                break

            # If the element is not on the screen, calculate the distance to center for scrolling
            element_center_y = element_top + (element_height / 2)
            screen_center_y = viewport_height / 2
            distance_to_center = element_center_y - screen_center_y

            # If we are already very close to the center, stop
            if abs(distance_to_center) < random.randint(40, 80):
                break

            scroll_step: int
            if distance_to_center > 0:
                # Scroll down (target below screen)
                scroll_step = random.randint(150, 350)
            else:
                # Scroll up (target above screen)
                scroll_step = random.randint(-350, -150)

            self.page.mouse.wheel(0, scroll_step)
            self.wait(*wait_ms)

        self.wait(300, 600)
        self.wait(*wait_ms)

    def _typo_effect(
        self,
        char: str,
        typo_chance: float,
        wait_ms: tuple[int, int] = WAIT_MS,
    ) -> None:
        # Logic for random typo (don't break spaces)
        if char == " " or random.random() >= typo_chance:
            return

        pool = ""
        for s_set in self.typo_char_sets.values():
            if char in s_set:
                pool = s_set
                break

        # If the symbol is rare and is not in the pools, we create a default list (letters + numbers)
        if not pool:
            pool: str = self.typo_char_sets["eng_lower"] + self.typo_char_sets["digits"]

        valid_choices: list[str] = [c for c in pool if c != char]
        if not valid_choices:
            log.warning(f"No valid choices found for character {char!r}.")
            return

        wrong_char: str = random.choice(valid_choices)

        self.page.keyboard.type(wrong_char)
        self.wait(60, 140)
        self.wait(180, 350)  # Pause for recognizing the error
        self.page.keyboard.press("Backspace")
        self.wait(*wait_ms)

    def type_text(
        self,
        locator: Locator | str,
        text: str,
        typo_chance: float = 0.07,
        max_attempts: int = 3,
        strict_validation: bool = False,
        wait_ms: tuple[int, int] = WAIT_MS,
    ) -> bool:
        """
        Types text like a human: with unique pauses, random typos,
        deletion of them through Backspace and final validation of the input value.
        """

        if isinstance(locator, str):
            locator = self.page.locator(locator)

        log.info(f"Typing text ({len(text)}): {text!r}, locator: {locator}")

        for attempt in range(1, max_attempts + 1):
            # Click on the field to bring focus
            self.click(locator)

            # Realistically clear the field through keyboard emulation of Ctrl+A -> Backspace
            self.page.keyboard.down("Control")
            self.page.keyboard.press("a")
            self.page.keyboard.up("Control")
            self.page.keyboard.press("Backspace")
            self.wait(*wait_ms)

            # Typing character by character
            for char in text:
                self._typo_effect(char, typo_chance=typo_chance, wait_ms=wait_ms)

                # Type correct character
                self.page.keyboard.type(char)

                # Typing rhythm (delay between keys)
                random_delay: int = random.randint(50, 160)
                # 4% chance that the person thought about a word in the middle of it
                if random.random() < 0.04:
                    random_delay += random.randint(350, 700)
                self.page.wait_for_timeout(random_delay)

            # Validate the actually typed text in the field
            actual_text: str = locator.input_value() or ""

            is_valid: bool
            if strict_validation:
                is_valid = actual_text == text
            else:

                def _remove_all_spaces(text: str) -> str:
                    return re.sub(r"\s+", "", text)

                is_valid = _remove_all_spaces(actual_text) == _remove_all_spaces(text)

            if is_valid:
                return True

            log.warning(f"Expected text {text!r}, but got {actual_text!r}.")

            self.wait(400, 800)

        raise RuntimeError(
            f"Failed to correctly type {text!r} after {max_attempts} attempts."
        )

    def move_mouse_to_center(self) -> None:
        """
        Smoothly moves the mouse cursor to a random area around the center of the screen.
        Takes: page (a Playwright page object)
        """

        # Move the cursor along a human-like trajectory
        point: Point = get_center_page(self.page)
        self.cursor.move_to(point)

        # Simulate a small pause after movement (200-600 ms)
        self.wait(200, 600)

    def ensure_change_url(
        self,
        action: Callable[[], None],
        is_ok_url: Callable[[str], bool],
        max_attempts: int = 3,
    ) -> None:
        prev_url: str = self.page.url
        log.info(f"Current URL: {prev_url!r}")

        attempt: int = 0
        while True:
            # If the URL substring is found and the URL has changed
            if is_ok_url(self.page.url) and prev_url != self.page.url:
                break

            try:
                action()

                log.info("Waiting for url load")
                self.page.wait_for_url(
                    is_ok_url, timeout=5_000, wait_until="domcontentloaded"
                )
                log.info(f"Page changed! New URL: {self.page.url!r}")

                break

            except Exception:
                log.exception("Error:")
                log.info("Trying to move the cursor and retry")
                attempt += 1
                self.cursor.move_to(
                    {
                        "x": 10 + random.randint(-10, 10),
                        "y": 500 + random.randint(-100, 100),
                    }
                )
                if attempt == max_attempts:
                    log.info(f"Loading {prev_url!r}")
                    attempt = 0
                    self.page.goto(prev_url)
                self.wait(4_000, 5_000)
