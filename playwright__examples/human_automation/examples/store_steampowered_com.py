#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# playwright>=1.61.0
from playwright.sync_api import sync_playwright

from human_automation.human_automation import HumanAutomation

URL: str = "https://store.steampowered.com/"


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    human_automation = HumanAutomation(page)

    page.goto(URL, wait_until="domcontentloaded")

    categories_locator = page.get_by_label("Меню магазина").locator(
        "button > div:has-text('Категории')"
    )
    print(categories_locator)
    human_automation.click(categories_locator)

    # View all tags
    all_tags_locator = page.locator("a:has-text('Просмотреть все метки')")
    print(all_tags_locator)
    human_automation.click(all_tags_locator)

    # Free To Play
    free_to_play_locator = page.get_by_role("button", name="Бесплатная игра")
    print(categories_locator)
    human_automation.click(free_to_play_locator)

    go_to_free_to_play_locator = page.get_by_text("Просмотреть все")
    print(go_to_free_to_play_locator)
    human_automation.click(go_to_free_to_play_locator)

    filters_locator = page.locator("//div[text()='Фильтры']/..").first
    print(filters_locator)
    human_automation.move_to(filters_locator)

    genres_frame_locator = filters_locator.locator("//div[text()='Жанры']/../..").first
    print(genres_frame_locator)
    human_automation.move_to(genres_frame_locator)

    genres_locator = genres_frame_locator.locator("//div[text()='Жанры']")
    print(genres_locator)
    human_automation.click(genres_locator)

    genres_all_locator = genres_frame_locator.locator("//div[text()='Показать больше']")
    print(genres_all_locator)
    human_automation.click(genres_all_locator)

    genre_shooter_locator = genres_frame_locator.locator("//div/a[text()='Шутер']")
    print(genre_shooter_locator)
    human_automation.click(genre_shooter_locator)

    sub_genres_frame_locator = filters_locator.locator(
        "//div[text()='Поджанры']/../.."
    ).first
    print(sub_genres_frame_locator)
    human_automation.move_to(sub_genres_frame_locator)

    genres_locator = sub_genres_frame_locator.locator("//div[text()='Поджанры']")
    print(genres_locator)
    human_automation.click(genres_locator)

    sub_genres_all_locator = sub_genres_frame_locator.locator(
        "//div[text()='Показать больше']"
    )
    print(sub_genres_all_locator)
    human_automation.click(sub_genres_all_locator)

    fps_locator = sub_genres_frame_locator.locator(
        "//div/a[text()='Шутер от первого лица']"
    )
    print(fps_locator)
    human_automation.click(fps_locator)

    human_automation.click(page.get_by_role("button", name="Показать больше"))

    human_automation.move_to(
        page.locator("a[href *= '/app/'][role='button']:has(img[alt]):visible").first
    )
    human_automation.wait(2_000, 4_000)

    for locator in page.locator(
        "a[href *= '/app/'][role='button']:has(img[alt]):visible"
    ).all():
        print(locator)

        name: str = locator.locator("img[alt]").get_attribute("alt")
        URL: str = locator.get_attribute("href")
        print(f"{name!r}: {URL}")

        human_automation.move_to(locator)

        print()

    page.wait_for_timeout(5_000)
