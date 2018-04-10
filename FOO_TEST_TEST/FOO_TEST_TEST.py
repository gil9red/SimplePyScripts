#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


# Fingerprinting with Zero-Width Characters

# zero-width-detection
# https://medium.com/@umpox/be-careful-what-you-copy-invisibly-inserting-usernames-into-text-with-zero-width-characters-18b4e6f17b66
# https://habrahabr.ru/post/352950/

# https://github.com/umpox/zero-width-detection
# DEMO: https://umpox.github.io/zero-width-detection/


# SOURCE: https://habrahabr.ru/post/352950/#comment_10745120
# const zeroWidthSpace = '\u200B';        // 8203
# const zeroWidthNonJoiner = '\u200C';    // 8204
# const zeroWidthJoiner = '\u200D';       // 8205
# const zeroWidthNoBreakSpace = '\uFEFF'; // 65279


# SOURCE: https://github.com/umpox/zero-width-detection/blob/master/src/utils/usernameToZeroWidth.js
# const zeroPad = num => '00000000'.slice(String(num).length) + num;
#
# const textToBinary = username => (
#   username.split('').map(char => zeroPad(char.charCodeAt(0).toString(2))).join(' ')
# );
#
# const binaryToZeroWidth = binary => (
#   binary.split('').map((binaryNum) => {
#     const num = parseInt(binaryNum, 10);
#     if (num === 1) {
#       return '​'; // invisible &#8203;
#     } else if (num === 0) {
#       return '‌'; // invisible &#8204;
#     }
#     return '‍'; // invisible &#8205;
#   }).join('﻿') // invisible &#65279;
# );
#
# export default (username) => {
#   const binaryUsername = textToBinary(username);
#   const zeroWidthUsername = binaryToZeroWidth(binaryUsername);
#   return zeroWidthUsername;
# };


ZERO_WIDTH_SPACE = '\u200B'  # 8203
ZERO_WIDTH_NON_JOINER = '\u200C'  # 8204
ZERO_WIDTH_JOINER = '\u200D'  # 8205
ZERO_WIDTH_NO_BREAK_SPACE = '\uFEFF'  # 65279


def to_binary(c: str) -> str:
    return bin(ord(c))[2:].zfill(8)


def text_to_binary(username: str) -> str:
    return ' '.join(map(to_binary, username))


def binary_to_zero_width(binary_username: str) -> str:
    zero_width_items = []

    for c in binary_username:
        if c == '1':
            zero_width = ZERO_WIDTH_SPACE
        elif c == '0':
            zero_width = ZERO_WIDTH_NON_JOINER
        else:
            zero_width = ZERO_WIDTH_JOINER

        zero_width_items.append(zero_width)

    return ZERO_WIDTH_NO_BREAK_SPACE.join(zero_width_items)


def username_to_zero_width(username: str) -> str:
    binary_username = text_to_binary(username)
    zero_width_username = binary_to_zero_width(binary_username)
    return zero_width_username


def append_fingerprint_to_text(text: str, username: str) -> str:
    left_half = len(text) // 2
    return text[:left_half] + username_to_zero_width(username) + text[left_half:]


#########


# SOURCE: https://github.com/umpox/zero-width-detection/blob/master/src/utils/zeroWidthToUsername.js
# const zeroWidthToBinary = string => (
#   string.split('﻿').map((char) => { // invisible &#65279;
#     if (char === '​') { // invisible &#8203;
#       return '1';
#     } else if (char === '‌') { // invisible &#8204;
#       return '0';
#     }
#     return ' '; // split up binary with spaces;
#   }).join('')
# );
#
# const binaryToText = string => (
#   string.split(' ').map(num => String.fromCharCode(parseInt(num, 2))).join('')
# );
#
# export default (zeroWidthUsername) => {
#   const binaryUsername = zeroWidthToBinary(zeroWidthUsername);
#   const textUsername = binaryToText(binaryUsername);
#   return textUsername;
# };


def zero_width_to_binary(text: str) -> str:
    binary = []

    for c in text.split(ZERO_WIDTH_NO_BREAK_SPACE):
        if c == ZERO_WIDTH_SPACE:
            binary.append('1')
        elif c == ZERO_WIDTH_NON_JOINER:
            binary.append('0')
        else:
            binary.append(' ')

    return ''.join(binary)


def binary_to_text(text: str) -> str:
    return ''.join(chr(int(num, 2)) for num in text.split(' '))


def get_zero_width_from_text(text: str) -> str:
    return ''.join(
        c for c in text
        if c in (ZERO_WIDTH_SPACE, ZERO_WIDTH_NON_JOINER, ZERO_WIDTH_JOINER, ZERO_WIDTH_NO_BREAK_SPACE)
    )


def get_username_from_zero_width_username(zero_width_username: str) -> str:
    binary_username = zero_width_to_binary(zero_width_username)
    text_username = binary_to_text(binary_username)
    return text_username


def get_username_from_text(text: str) -> str:
    zero_width_username = get_zero_width_from_text(text)
    binary_username = zero_width_to_binary(zero_width_username)
    text_username = binary_to_text(binary_username)
    return text_username


if __name__ == '__main__':
    text = "This is some confidential text that you really shouldn't be sharing anywhere else. " \
           "Это конфиденциальный текст, которым вы действительно не должны делиться."
    username = 'hello world/привет мир'

    print(len(text), text)

    text_zero_width = append_fingerprint_to_text(text, username)
    print(len(text_zero_width), text_zero_width)
    print(repr(text_zero_width))
    print()

    zero_width_username_1 = username_to_zero_width(username)
    zero_width_username_2 = get_zero_width_from_text(text_zero_width)
    print(zero_width_username_1 == zero_width_username_2)
    print()

    user_name = get_username_from_zero_width_username(zero_width_username_2)
    print(user_name)

    user_name = get_username_from_text(text_zero_width)
    print(user_name)


quit()

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
