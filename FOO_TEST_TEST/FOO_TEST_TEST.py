#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# driver = webdriver.Firefox()
# driver.get("https://grouple.co/")
# # driver.maximize_window()
#
#
# last_height = driver.execute_script("return document.body.scrollHeight")
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#
# # element = driver.find_element_by_css_selector('.pagination')
# # print(element)
# #
# # # wait for then hover it
# # element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".pagination")))
# # print(element)
# #
# # ActionChains(driver).move_to_element(element).perform()
#
# # # wait for Fastrack menu item to appear, then click it
# # fastrack = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[@data-tracking-id='0_Fastrack']")))
# # fastrack.click()
#
# quit()

# pip install selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# # get the Firefox profile object
# firefox_profile = webdriver.FirefoxProfile()
#
# # Disable CSS
# firefox_profile.set_preference('permissions.default.stylesheet', 2)
#
# # Disable images
# firefox_profile.set_preference('permissions.default.image', 2)
#
# # Disable Flash
# firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
#
# driver = webdriver.Firefox(firefox_profile=firefox_profile)
driver = webdriver.Firefox()
driver.implicitly_wait(10)  # seconds
driver.get('https://pikabu.ru/story/ii_pobedil_5467581')
print('Title: "{}"'.format(driver.title))

wait = WebDriverWait(driver, timeout=10)

# last_height = driver.execute_script("return document.body.scrollHeight")
# print('last_height:', last_height)
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

more_comment = wait.until(
    EC.visibility_of_element_located((By.CLASS_NAME, 'b-comment-toggle_type_expand'))
)
while True:
    try:
        more_comment = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'b-comments__next'))
        )
        print(more_comment, more_comment.location, more_comment.text)
        more_comment.click()

        import time
        time.sleep(2)

    except TimeoutException as e:
        print('TimeoutException:', e)
        break
i = 1
for element in driver.find_elements_by_class_name('b-comment-toggle_type_expand'):
    if element.is_displayed():
        print(i, element, element.location, element.text)
        i += 1
driver.quit()
quit()

body = driver.find_element_by_tag_name('body')

while True:
    while True:
        try:
            more_comment = wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'b-comment-toggle_type_expand'))
            )
            print(more_comment, more_comment.location, more_comment.text)
            more_comment.click()
            # ActionChains(driver).move_to_element(more_comment).click(more_comment).perform()

            import time
            time.sleep(2)

        except TimeoutException as e:
            print('TimeoutException:', e)
            break

    body.send_keys(Keys.PAGE_DOWN)

    # while True:
    #     try:
    #         more_comment = wait.until(
    #             EC.visibility_of_element_located((By.CLASS_NAME, 'b-comments__next'))
    #         )
    #         print(more_comment, more_comment.location, more_comment.text)
    #         more_comment.click()
    #         # ActionChains(driver).move_to_element(more_comment).click(more_comment).perform()
    #
    #         import time
    #         time.sleep(2)
    #
    #     except TimeoutException as e:
    #         print('TimeoutException:', e)
    #         break


print('Finish')

# <div class="b-comment-toggle b-comment-toggle_type_expand b-comment-toggle_type_hidden" style="display: inline-block">
# <div class="b-comment-toggle__icon fa fa-plus-square"></div><div class="b-comment-toggle__count" style="display: block">ещё комментарии <span class="b-comment-toggle__count-text"></span> <i class="i-sprite--inline-block i-sprite--comments__show"></i></div></div>

# <div class="b-comment-toggle b-comment-toggle_type_expand" style="display: inline-block"><div class="b-comment-toggle__icon fa fa-plus-square"></div><div class="b-comment-toggle__count" style="display: block">раскрыть ветвь <span class="b-comment-toggle__count-text">1</span> <i class="i-sprite--inline-block i-sprite--comments__show"></i></div></div>
# <div class="b-comments__next">Ещё <span class="b-comments__next-count">400 комментариев</span> <i class="fa fa-refresh"></i> <span class="b-comments__next-error"></span></div>

# more_comment = wait.until(
#     EC.visibility_of_element_located((By.CLASS_NAME, 'b-comment-toggle__count'))
# )
# more_comments = driver.find_elements_by_class_name('b-comment-toggle__count')
# for more_comment in more_comments:
#     ActionChains(driver).move_to_element(more_comment).perform()
#
#     import time
#     time.sleep(4)


# i = 1
# for img in driver.find_elements_by_css_selector('img[data-large-image]'):
#     # print(img.get_attribute('src'), img.get_attribute('data-large-image'))
#     print(i, img.get_attribute('data-large-image'))
#     i += 1



# # Делаем скриншот результата
# driver.save_screenshot('before_search.png')
#
# driver.find_element_by_css_selector('input#search').send_keys('Funny cats' + Keys.RETURN)
#
# result_count = driver.find_element_by_id('result-count')
# print(result_count.text)
#
# print('Title: "{}"'.format(driver.title))
#
# # Делаем скриншот результата
# driver.save_screenshot('after_search.png')
#
# video_list = driver.find_elements_by_id('dismissable')
#
# # Click on random video
# import random
# random.choice(video_list).click()
#
# video = WebDriverWait(driver, timeout=10).until(
#     EC.visibility_of_element_located((By.TAG_NAME, 'video'))
# )
#
# video_title = driver.find_element_by_class_name('title')
# print('Title: "{}"'.format(driver.title))
# print('Video Title: "{}"'.format(video_title.text))
#
# driver.save_screenshot('final.png')

driver.quit()
