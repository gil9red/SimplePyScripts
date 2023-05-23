#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def get_urls(driver) -> list[str]:
    urls = []

    for link in driver.find_elements_by_css_selector(
        "figure.media-thumb.desktop link[itemprop=contentUrl]"
    ):
        url_gif = link.get_attribute("content")
        gif_id = url_gif.split("/")[-1]
        url_download = URL_DOWNLOAD_TEMPLATE + gif_id
        urls.append(url_download)

    return urls


URL_DOWNLOAD_TEMPLATE = "https://i.gifer.com/embedded/download/"


options = Options()
options.add_argument("--headless")

driver = webdriver.Firefox(options=options)
driver.get("https://gifer.com/ru/gifs/loading")

print(f'Title: "{driver.title}"')

driver.implicitly_wait(20)

urls = get_urls(driver)
print(f"{len(urls)}: {urls}")
# 4: ['https://i.gifer.com/embedded/download/g0R5.gif', 'https://i.gifer.com/embedded/download/VAyR.gif', 'https://i.gifer.com/embedded/download/ZKZx.gif', 'https://i.gifer.com/embedded/download/ZZ5H.gif']

# Small scroll down
driver.execute_script(f"window.scrollTo(0, 200);")

urls = get_urls(driver)
print(f"{len(urls)}: {urls}")
# 8: ['https://i.gifer.com/embedded/download/g0R5.gif', 'https://i.gifer.com/embedded/download/VAyR.gif', 'https://i.gifer.com/embedded/download/ZKZx.gif', 'https://i.gifer.com/embedded/download/ZZ5H.gif', 'https://i.gifer.com/embedded/download/g0R9.gif', 'https://i.gifer.com/embedded/download/ZWdx.gif', 'https://i.gifer.com/embedded/download/7pld.gif', 'https://i.gifer.com/embedded/download/AqCa.gif']

driver.quit()
