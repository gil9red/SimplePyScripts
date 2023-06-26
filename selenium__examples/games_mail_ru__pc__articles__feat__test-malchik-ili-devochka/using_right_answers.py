#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random
import time

# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By


RIGHT_ANSWERS = [
    "Разговор по душам между двумя мужчинами",
    "Длинными волосами эксперта не обмануть! Воистину мальчик",
    "Эта женщина всем покажет, где раки зимуют",
    "Заправский ловелас, который наверняка разбил не одно девичье сердечко",
    "Тренировки на свежем воздухе даже из девочки сделают качка",
    "Трудно поверить, но это мужчина!",
    "Привыкли к грудастым пираткам? Пора взглянуть реальности в лицо, сухопутные крысы",
    "Мужик! Как есть мужик!",
    "Кто скажет, что это мальчик, пусть первый бросит в меня камень, как говорил еще Остап Бендер!",
    "Очередная японская дева, маскирующаяся под мужика, несть им числа",
    "Настоящий мужчина, рыцарь до последней бусинки",
    "Мужик в бронелифчике, вот это да!",
]


driver = webdriver.Firefox()
driver.implicitly_wait(10)  # seconds
driver.get("https://games.mail.ru/pc/articles/feat/test-malchik-ili-devochka/")
print(f'Title: "{driver.title}"\n')

# Scroll to test
driver.execute_script(
    "arguments[0].scrollIntoView();", driver.find_element(By.ID, "js-pc__article__descr")
)

start_button = driver.find_element(By.CSS_SELECTOR, ".quiz__start-button")
start_button.click()

while True:
    time.sleep(1)

    quiz_count_el = driver.find_element(By.CLASS_NAME, "quiz__count")
    quiz_count_text = quiz_count_el.text
    print(quiz_count_text)

    answer_elements = driver.find_elements(By.CSS_SELECTOR, ".quiz__answer-text")
    print(f'Answers: {", ".join(repr(el.text.strip()) for el in answer_elements)}')

    selected_answer = None
    for el in answer_elements:
        answer = el.text.strip()
        if answer in RIGHT_ANSWERS:
            selected_answer = el
            break

    if selected_answer is None:
        print(f"Unknown answers. Select random answer")
        selected_answer = random.choice(answer_elements)

    print(f"Select answer: {selected_answer.text.strip()!r}")
    selected_answer.click()

    next_question_button = driver.find_element(By.CLASS_NAME, "quiz__next-question")
    next_question_button.click()

    print()

    # If last question
    # Example: 9/12
    start, end = quiz_count_text.split("/")
    if start == end:
        break

print("Result:")
print(driver.find_element(By.CLASS_NAME, "quiz__question").text)
print(driver.find_element(By.CLASS_NAME, "quiz__result").text)

# Title: "Тест: мальчик или девочка — Игры Mail.ru"
#
# 1/12
# Answers: 'Мальчик участливо подставляет плечо эльфиечке', 'Разговор по душам между двумя мужчинами', 'Две девушки обсуждают, что и когда в их жизни пошло не так'
# Select answer: 'Разговор по душам между двумя мужчинами'
#
# 2/12
# Answers: 'Сильная и независимая женщина может себе позволить закрытый костюм даже в jRPG', 'Длинными волосами эксперта не обмануть! Воистину мальчик'
# Select answer: 'Длинными волосами эксперта не обмануть! Воистину мальчик'
#
# 3/12
# Answers: 'Эта женщина всем покажет, где раки зимуют', 'Типичный смазливый недомужик из японской игры'
# Select answer: 'Эта женщина всем покажет, где раки зимуют'
#
# 4/12
# Answers: 'Сердитая, но все равно красивая девочка, которой постоянно приходится отбиваться от грубых мужиков', 'Заправский ловелас, который наверняка разбил не одно девичье сердечко'
# Select answer: 'Заправский ловелас, который наверняка разбил не одно девичье сердечко'
#
# 5/12
# Answers: 'Да пусть хоть бусы нацепит, по мускулатуре видно - мужик', 'Тренировки на свежем воздухе даже из девочки сделают качка'
# Select answer: 'Тренировки на свежем воздухе даже из девочки сделают качка'
#
# 6/12
# Answers: 'Трудно поверить, но это мужчина!', 'Соблазнительная красотка с волнующими формами (когда-нибудь, лет так через 10)'
# Select answer: 'Трудно поверить, но это мужчина!'
#
# 7/12
# Answers: 'Сефирот сильно изменился за лето, но все еще мужик', 'Привыкли к грудастым пираткам? Пора взглянуть реальности в лицо, сухопутные крысы'
# Select answer: 'Привыкли к грудастым пираткам? Пора взглянуть реальности в лицо, сухопутные крысы'
#
# 8/12
# Answers: 'Ну это уж точно девочка', 'Мужик! Как есть мужик!'
# Select answer: 'Мужик! Как есть мужик!'
#
# 9/12
# Answers: 'Кто скажет, что это мальчик, пусть первый бросит в меня камень, как говорил еще Остап Бендер!', 'Кто скажет, что это девочка, пусть тоже чем-нибудь в меня кинет!'
# Select answer: 'Кто скажет, что это мальчик, пусть первый бросит в меня камень, как говорил еще Остап Бендер!'
#
# 10/12
# Answers: 'Очередной японский подросток, тысячи их', 'Очередная японская дева, маскирующаяся под мужика, несть им числа'
# Select answer: 'Очередная японская дева, маскирующаяся под мужика, несть им числа'
#
# 11/12
# Answers: 'Прелестная дева в исполнении Еситаки Амано, известного японского иллюстратора', 'Настоящий мужчина, рыцарь до последней бусинки'
# Select answer: 'Настоящий мужчина, рыцарь до последней бусинки'
#
# 12/12
# Answers: 'Женщина в доспехах, эка невидаль', 'Мужик в бронелифчике, вот это да!'
# Select answer: 'Мужик в бронелифчике, вот это да!'
#
# Result:
# 12 баллов из 12!
# Браво! Вы — заслуженный эксперт по персонажам из японских ролевых игр!
