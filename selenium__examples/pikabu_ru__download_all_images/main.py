#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os.path
import time

from pathlib import Path
from urllib.request import urlretrieve

# pip install selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, MoveTargetOutOfBoundsException
from selenium.webdriver.common.action_chains import ActionChains


def get_suffix(url: str) -> str:
    return os.path.splitext(url)[1]


url = "https://pikabu.ru/story/ii_pobedil_5467581"
post_name = url.rstrip("/").split("/")[-1]
dir_name = Path(__file__).resolve().parent / post_name
dir_name.mkdir(exist_ok=True)

firefox_profile = webdriver.FirefoxProfile()

# Disable CSS
firefox_profile.set_preference("permissions.default.stylesheet", 2)

# Disable images
firefox_profile.set_preference("permissions.default.image", 2)

# Disable Flash
firefox_profile.set_preference("dom.ipc.plugins.enabled.libflashplayer.so", "false")

driver = webdriver.Firefox(firefox_profile=firefox_profile)

try:
    driver.set_page_load_timeout(10)
    # driver.implicitly_wait(10)  # Seconds

    try:
        driver.get(url)
    except TimeoutException:
        # Let's try to parse without waiting for a full load
        pass

    print(f"Title: {driver.title!r}")

    more_comments_el = driver.find_element_by_class_name("comments__more-button")
    section_after_comments_el = driver.find_element_by_css_selector(
        ".comments-wrapper ~ section"
    )

    num_click = 0
    y_position = 0

    # Load all comments
    while True:
        # Move down page to bottom comments
        while True:
            try:
                ActionChains(driver).move_to_element(
                    section_after_comments_el
                ).perform()
                break
            except MoveTargetOutOfBoundsException:
                y_position += 100
                driver.execute_script(f"window.scrollTo(0, {y_position});")

        if more_comments_el.is_displayed():
            ActionChains(driver).move_to_element(more_comments_el).click().perform()
            num_click += 1
            time.sleep(5)
            continue

        print(f"The number of clicks on a load comments: {num_click}")
        break

    print("Go search comments!")

    images = driver.find_elements_by_css_selector(".page-story img.story-image__image")
    num_images = len(images)

    for i, img_el in enumerate(images, 1):
        img_url = img_el.get_attribute("data-large-image")

        num_img = f"_{i}" if len(images) > 1 else ""
        file_name = dir_name / f"__story{num_img}{get_suffix(img_url)}"
        urlretrieve(img_url, file_name)

    for comment_el in driver.find_elements_by_css_selector(
        "div.page-story__comments div.comment"
    ):
        comment_id = comment_el.get_attribute("id")

        comment_body_el = comment_el.find_element_by_class_name("comment__body")
        user_name = comment_body_el.find_element_by_css_selector(
            ".comment__user"
        ).get_attribute("data-name")
        # print(user_name, comment_id)

        images = comment_body_el.find_elements_by_css_selector(
            "div.comment-image__content > a > img"
        )
        num_images += len(images)

        for i, img_el in enumerate(images, 1):
            img_url = img_el.get_attribute("data-large-image")

            num_img = f"_{i}" if len(images) > 1 else ""
            file_name = (
                dir_name / f"{user_name}__{comment_id}{num_img}{get_suffix(img_url)}"
            )
            urlretrieve(img_url, file_name)

    print(f"Found images: {num_images}")

finally:
    driver.quit()
