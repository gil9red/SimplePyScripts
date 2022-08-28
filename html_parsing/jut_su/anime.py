#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
import time

from dataclasses import dataclass
from urllib.parse import urljoin
from typing import Iterator

import requests
from bs4 import BeautifulSoup

from common import session


RE_ANIME_PAGE_NEXT = re.compile('anime_page_next = (true|false);')

URL = 'https://jut.su/anime/'


@dataclass
class Anime:
    url: str
    title: str


def parse_anime_list(rs: requests.Response) -> list[Anime]:
    items = []
    root = BeautifulSoup(rs.text, 'html.parser')
    for anime_el in root.select('.all_anime_global'):
        url = urljoin(rs.url, anime_el.a['href'])
        title = anime_el.select_one('.aaname').text

        items.append(Anime(url, title))

    return items


def send_get() -> requests.Response:
    rs = session.get(URL)
    rs.raise_for_status()

    return rs


def send_post(
        page: int = 1,
        show_search: str = '',
        anime_of_user: str = ''
) -> requests.Response:
    headers = {
        'X-Requested-With': 'XMLHttpRequest'
    }
    data = {
        'ajax_load': 'yes',
        'start_from_page': page,
        'show_search': show_search,
        'anime_of_user': anime_of_user,
    }
    rs = session.post(URL, data=data, headers=headers)
    rs.raise_for_status()

    return rs


def has_next_page(text: str) -> bool:
    m = RE_ANIME_PAGE_NEXT.search(text)
    if not m:
        raise Exception('Не удалось найти переменную anime_page_next!')
    return m.group(1) == 'true'


def get_all_lazy() -> Iterator[list[Anime]]:
    page = 1

    while True:
        # На первый раз GET, на последующие: POST, притворяясь ajax
        if page == 1:
            rs = send_get()
        else:
            time.sleep(1)
            rs = send_post(page=page)

        yield parse_anime_list(rs)

        if not has_next_page(rs.text):
            break

        page += 1


def get_all() -> list[Anime]:
    items = []
    for anime_list in get_all_lazy():
        items += anime_list
    return items


if __name__ == '__main__':
    # Первые 3 страницы
    for page, anime_list in enumerate(get_all_lazy(), 1):
        print(page, anime_list)
        if page == 3:
            break
    """
    1 [Anime(url='https://jut.su/shingekii-no-kyojin/', title='Атака титанов'), Anime(url='https://jut.su/full-metal-alchemist/', title='Стальной алхимик'), Anime(url='https://jut.su/onepunchman/', title='Ванпанчмен'), Anime(url='https://jut.su/sword-arts-online/', title='Мастера меча онлайн'), Anime(url='https://jut.su/boku-hero-academia/', title='Моя геройская академия'), Anime(url='https://jut.su/tokushu/', title='Токийский Гуль'), Anime(url='https://jut.su/kimetsu-yaiba/', title='Клинок, рассекающий демонов'), Anime(url='https://jut.su/hunter-hunter/', title='Хантер х Хантер'), Anime(url='https://jut.su/stein-gate/', title='Врата Штейна'), Anime(url='https://jut.su/life-no-game/', title='Нет игры - нет жизни'), Anime(url='https://jut.su/code-geass/', title='Код Гиас'), Anime(url='https://jut.su/toradora/', title='ТораДора'), Anime(url='https://jut.su/noragaami/', title='Бездомный Бог'), Anime(url='https://jut.su/re-zerou-kara/', title='С нуля: Пособие по выживанию в альтернативном мире'), Anime(url='https://jut.su/jujutsu-kaisen/', title='Магическая битва'), Anime(url='https://jut.su/oneepiece/', title='Ван Пис'), Anime(url='https://jut.su/angela-beats/', title='Ангельские ритмы!'), Anime(url='https://jut.su/akaame-ga-kill/', title='Убийца Акаме!'), Anime(url='https://jut.su/nanatsu-taizai/', title='Семь смертных грехов'), Anime(url='https://jut.su/boku-dake/', title='Город, в котором меня нет'), Anime(url='https://jut.su/mirai-nikki/', title='Дневник будущего'), Anime(url='https://jut.su/roomination/', title='Класс убийц'), Anime(url='https://jut.su/mob-100/', title='Моб Психо 100'), Anime(url='https://jut.su/ao-exorcist/', title='Синий Экзорцист'), Anime(url='https://jut.su/haaikyu/', title='Волейбол!'), Anime(url='https://jut.su/kono-subarashii/', title='Этот прекрасный мир'), Anime(url='https://jut.su/yakusoku-neverland/', title='Обещанный Неверленд'), Anime(url='https://jut.su/bleeach/', title='Блич'), Anime(url='https://jut.su/kiseijuu/', title='Паразит'), Anime(url='https://jut.su/cowboy-bebop/', title='Ковбой Бибоп')]
    2 [Anime(url='https://jut.su/faairytail/', title='Фейри Тейл'), Anime(url='https://jut.su/neon-evangelion/', title='Евангелион'), Anime(url='https://jut.su/death-parade/', title='Парад смерти'), Anime(url='https://jut.su/vioulet-evergarden/', title='Вайолет Эвергарден'), Anime(url='https://jut.su/another/', title='Другая'), Anime(url='https://jut.su/shokugeki-no-souma/', title='Повар-боец Сома'), Anime(url='https://jut.su/seishun-buta/', title='Этот глупый свин не понимает мечту девочки-зайки'), Anime(url='https://jut.su/soul-eater/', title='Пожиратель душ'), Anime(url='https://jut.su/psycho-pass/', title='Психопаспорт'), Anime(url='https://jut.su/dr-stoune/', title='Доктор Стоун'), Anime(url='https://jut.su/mada-shiranai/', title='Невиданный цветок'), Anime(url='https://jut.su/kaguya-sama/', title='Госпожа Кагуя: в любви как на войне'), Anime(url='https://jut.su/gurren-lagan/', title='Гуррен-Лаганн'), Anime(url='https://jut.su/darling-in-the-franxx/', title='Милый во Франксе'), Anime(url='https://jut.su/jojo-bizarre-adventure/', title='Невероятные приключения ДжоДжо'), Anime(url='https://jut.su/hataraku-maou-sama/', title='Сатана на подработке!'), Anime(url='https://jut.su/black-clouver/', title='Чёрный клевер'), Anime(url='https://jut.su/overlord/', title='Повелитель'), Anime(url='https://jut.su/danmachi/', title='Может, я встречу тебя в подземелье?'), Anime(url='https://jut.su/fate-zer-o/', title='Судьба: Начало'), Anime(url='https://jut.su/tate-yuusha-nariagari/', title='Восхождение героя щита'), Anime(url='https://jut.su/clanad/', title='Кланнад'), Anime(url='https://jut.su/kakeguruui/', title='Безумный азарт'), Anime(url='https://jut.su/durara/', title='Дюрарара!!'), Anime(url='https://jut.su/monogatari-series/', title='Цикл историй'), Anime(url='https://jut.su/yahari-ore-no-seishun/', title='Розовая пора моей школьной жизни сплошной обман'), Anime(url='https://jut.su/chuunibyou-demo/', title='Чудачества любви не помеха'), Anime(url='https://jut.su/hyouka/', title='Хьёка'), Anime(url='https://jut.su/slime-datta-ken/', title='О моём перерождении в слизь'), Anime(url='https://jut.su/owari-no-seraph/', title='Последний Серафим')]
    3 [Anime(url='https://jut.su/bungo-stray-dogs/', title='Бродячие псы: Литературные гении'), Anime(url='https://jut.su/made-abyss/', title='Сделано в Бездне'), Anime(url='https://jut.su/madoka-magica/', title='Волшебница Мадока Магика'), Anime(url='https://jut.su/vinland-saga/', title='Сага о Винланде'), Anime(url='https://jut.su/pet-na-kanojo/', title='Кошечка из Сакурасо'), Anime(url='https://jut.su/deadman-wonderland/', title='Страна чудес смертников'), Anime(url='https://jut.su/kaichou-wa-maid/', title='Президент - горничная!'), Anime(url='https://jut.su/guilty-crown/', title='Корона Грешника'), Anime(url='https://jut.su/enen-no-shouboutai/', title='Пламенная бригада пожарных'), Anime(url='https://jut.su/samurai-champlo/', title='Самурай Чамплу'), Anime(url='https://jut.su/dragonball/', title='Драгонболл'), Anime(url='https://jut.su/kobayashi/', title='Дракон-горничная Кобаяши'), Anime(url='https://jut.su/kuroshitsuuji/', title='Темный дворецкий'), Anime(url='https://jut.su/kuroko-no-basuke/', title='Баскетбол Куроко'), Anime(url='https://jut.su/horimiya/', title='Хоримия'), Anime(url='https://jut.su/nisekooi/', title='Притворная любовь'), Anime(url='https://jut.su/kyoukai-kanata/', title='За гранью'), Anime(url='https://jut.su/zankyou-no-terror/', title='Эхо террора'), Anime(url='https://jut.su/douroro/', title='Дороро'), Anime(url='https://jut.su/login-horizon/', title='Логин Горизонт'), Anime(url='https://jut.su/host-club/', title='Хост-клуб Оранской школы'), Anime(url='https://jut.su/tokyo-reveengers/', title='Токийские мстители'), Anime(url='https://jut.su/shugi-no-kyoushitsu/', title='Класс превосходства'), Anime(url='https://jut.su/mushoku-tensei/', title='Реинкарнация безработного'), Anime(url='https://jut.su/spy-family/', title='Семья шпиона'), Anime(url='https://jut.su/kaibutsu-kun/', title='Монстр за соседней партой'), Anime(url='https://jut.su/goblin-slayer/', title='Убийца гоблинов'), Anime(url='https://jut.su/unlimited-blade-works/', title='Клинков бесконечный край'), Anime(url='https://jut.su/k-on/', title='К-он!'), Anime(url='https://jut.su/mahouka-koukou-no-rettousei/', title='Непутёвый ученик в школе магии')]
    """

    all_anime = get_all()
    print(f'All anime ({len(all_anime)}): [{all_anime[0]}, ..., {all_anime[-1]}]')
    # All anime (863): [Anime(url='https://jut.su/shingekii-no-kyojin/', title='Атака титанов'), ..., Anime(url='https://jut.su/extreme-hearts/', title='Экстремальные сердца')]
