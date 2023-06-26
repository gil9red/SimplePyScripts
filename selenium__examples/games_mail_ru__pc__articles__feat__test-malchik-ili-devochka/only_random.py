#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random
import time

# pip install selenium
from selenium import webdriver


driver = webdriver.Firefox()
driver.implicitly_wait(10)  # seconds
driver.get("https://games.mail.ru/pc/articles/feat/test-malchik-ili-devochka/")
print(f'Title: "{driver.title}"\n')

# Scroll to test
driver.execute_script(
    "arguments[0].scrollIntoView();", driver.find_element_by_id("js-pc__article__descr")
)

start_button = driver.find_element_by_css_selector(".quiz__start-button")
start_button.click()

while True:
    time.sleep(1)

    quiz_count_el = driver.find_element_by_class_name("quiz__count")
    quiz_count_text = quiz_count_el.text
    print(quiz_count_text)

    answer_elements = driver.find_elements_by_css_selector(".quiz__answer-text")
    print(f'Answers: {", ".join(repr(el.text.strip()) for el in answer_elements)}')

    print("Select random answer")
    selected_answer = random.choice(answer_elements)

    print(f"Select answer: {selected_answer.text.strip()!r}")
    selected_answer.click()

    next_question_button = driver.find_element_by_class_name("quiz__next-question")
    next_question_button.click()

    print()

    # If last question
    # Example: 9/12
    start, end = quiz_count_text.split("/")
    if start == end:
        break

print("Result:")
print(driver.find_element_by_class_name("quiz__question").text)
print(driver.find_element_by_class_name("quiz__result").text)

# Title: "Тест: мальчик или девочка — Игры Mail.ru"
#
# 1/12
# Answers: 'Мальчик участливо подставляет плечо эльфиечке', 'Разговор по душам между двумя мужчинами', 'Две девушки обсуждают, что и когда в их жизни пошло не так'
# Select random answer
# Select answer: 'Разговор по душам между двумя мужчинами'
#
# 2/12
# Answers: 'Сильная и независимая женщина может себе позволить закрытый костюм даже в jRPG', 'Длинными волосами эксперта не обмануть! Воистину мальчик'
# Select random answer
# Select answer: 'Сильная и независимая женщина может себе позволить закрытый костюм даже в jRPG'
#
# 3/12
# Answers: 'Эта женщина всем покажет, где раки зимуют', 'Типичный смазливый недомужик из японской игры'
# Select random answer
# Select answer: 'Эта женщина всем покажет, где раки зимуют'
#
# 4/12
# Answers: 'Сердитая, но все равно красивая девочка, которой постоянно приходится отбиваться от грубых мужиков', 'Заправский ловелас, который наверняка разбил не одно девичье сердечко'
# Select random answer
# Select answer: 'Заправский ловелас, который наверняка разбил не одно девичье сердечко'
#
# 5/12
# Answers: 'Да пусть хоть бусы нацепит, по мускулатуре видно - мужик', 'Тренировки на свежем воздухе даже из девочки сделают качка'
# Select random answer
# Select answer: 'Да пусть хоть бусы нацепит, по мускулатуре видно - мужик'
#
# 6/12
# Answers: 'Трудно поверить, но это мужчина!', 'Соблазнительная красотка с волнующими формами (когда-нибудь, лет так через 10)'
# Select random answer
# Select answer: 'Соблазнительная красотка с волнующими формами (когда-нибудь, лет так через 10)'
#
# 7/12
# Answers: 'Сефирот сильно изменился за лето, но все еще мужик', 'Привыкли к грудастым пираткам? Пора взглянуть реальности в лицо, сухопутные крысы'
# Select random answer
# Select answer: 'Сефирот сильно изменился за лето, но все еще мужик'
#
# 8/12
# Answers: 'Ну это уж точно девочка', 'Мужик! Как есть мужик!'
# Select random answer
# Select answer: 'Мужик! Как есть мужик!'
#
# 9/12
# Answers: 'Кто скажет, что это мальчик, пусть первый бросит в меня камень, как говорил еще Остап Бендер!', 'Кто скажет, что это девочка, пусть тоже чем-нибудь в меня кинет!'
# Select random answer
# Select answer: 'Кто скажет, что это мальчик, пусть первый бросит в меня камень, как говорил еще Остап Бендер!'
#
# 10/12
# Answers: 'Очередной японский подросток, тысячи их', 'Очередная японская дева, маскирующаяся под мужика, несть им числа'
# Select random answer
# Select answer: 'Очередная японская дева, маскирующаяся под мужика, несть им числа'
#
# 11/12
# Answers: 'Прелестная дева в исполнении Еситаки Амано, известного японского иллюстратора', 'Настоящий мужчина, рыцарь до последней бусинки'
# Select random answer
# Select answer: 'Прелестная дева в исполнении Еситаки Амано, известного японского иллюстратора'
#
# 12/12
# Answers: 'Женщина в доспехах, эка невидаль', 'Мужик в бронелифчике, вот это да!'
# Select random answer
# Select answer: 'Женщина в доспехах, эка невидаль'
#
# Result:
# 6 баллов из 12!
# Вы на правильном пути, но Клауд все еще может обвести вас вокруг пальца.
