#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


@dataclass
class Meme:
    title: str
    url: str
    url_img: str


def get_memes_words(page: int = 1) -> list[Meme]:
    url = "https://memepedia.ru/category/memes/word/"
    if page > 1:
        url = f"{url}page/{page}/"

    rs = requests.get(url)
    rs.raise_for_status()

    items: list[Meme] = []

    root = BeautifulSoup(rs.content, "html.parser")
    for a in root.select(
        "#post-items .category-word > .post-thumbnail > a[href][title]"
    ):
        url_img = urljoin(rs.url, a.select_one("img[src]")["src"])
        items.append(
            Meme(
                title=a["title"],
                url=a["href"],
                url_img=url_img,
            )
        )

    return items


if __name__ == "__main__":
    memes_words: list[Meme] = get_memes_words()
    print(f"Memes Words page 1 ({len(memes_words)}):")
    for meme in memes_words:
        print(f"  {meme}")

    print()

    memes_words: list[Meme] = get_memes_words(page=2)
    print(f"Memes Words page 2 ({len(memes_words)}):")
    for meme in memes_words:
        print(f"  {meme}")
    """ 
    Memes Words page 1 (15):
      Meme(title='Обоюдно', url='https://memepedia.ru/oboyudno/', url_img='https://memepedia.ru/wp-content/uploads/2025/01/obojudno-360x270.jpg')
      Meme(title='Карась дуреет', url='https://memepedia.ru/karas-dureet/', url_img='https://memepedia.ru/wp-content/uploads/2024/12/karas-sdurel-360x270.jpg')
      Meme(title='Советское качество', url='https://memepedia.ru/sovetskoe-kachestvo/', url_img='https://memepedia.ru/wp-content/uploads/2024/11/cr-360x270.jpg')
      Meme(title='Вам чай с сахаром или с моими слезами?', url='https://memepedia.ru/vam-chaj-s-saxarom-ili-s-moimi-slezami/', url_img='https://memepedia.ru/wp-content/uploads/2024/11/fo7mmmdqciq-360x270.jpg')
      Meme(title='Терпим карлики', url='https://memepedia.ru/terpim-karliki/', url_img='https://memepedia.ru/wp-content/uploads/2024/11/terpim-karliki-mem-360x270.jpg')
      Meme(title='Неплох в области так сказать', url='https://memepedia.ru/neplox-v-oblasti-tak-skazat/', url_img='https://memepedia.ru/wp-content/uploads/2024/11/gz_-cv3weaastsc-360x270.jpeg')
      Meme(title='Щавель, ракушка, палитра, гитара', url='https://memepedia.ru/shhavel-rakushka-palitra-gitara/', url_img='https://memepedia.ru/wp-content/uploads/2024/09/palitra-gitara-360x270.jpg')
      Meme(title='Найк про', url='https://memepedia.ru/najk-pro/', url_img='https://memepedia.ru/wp-content/uploads/2024/09/najk-pro-mem-360x270.jpg')
      Meme(title='Пикми', url='https://memepedia.ru/pikmi/', url_img='https://memepedia.ru/wp-content/uploads/2024/09/pikmi-360x270.jpg')
      Meme(title='Мне не 20, мне 27, шалава', url='https://memepedia.ru/mne-ne-20-mne-27-shalava/', url_img='https://memepedia.ru/wp-content/uploads/2024/09/hq720-360x270.jpg')
      Meme(title='Суджа', url='https://memepedia.ru/sudzha/', url_img='https://memepedia.ru/wp-content/uploads/2024/08/ahrk-kygrhmoewokj3neo8ntclpo2u9bs7kx0fejholhjzvda-lyy9e82rshxsankxw89o4xxxuhl3yorew4l1hc-360x270.jpg')
      Meme(title='Чезабретто', url='https://memepedia.ru/chezabretto/', url_img='https://memepedia.ru/wp-content/uploads/2024/07/chezabretto-360x270.jpg')
      Meme(title='Вы будете кушать угощения', url='https://memepedia.ru/vy-budete-kushat-ugoshheniya/', url_img='https://memepedia.ru/wp-content/uploads/2024/07/ugoshchenija-360x270.jpg')
      Meme(title='Оплата у психолога прошла', url='https://memepedia.ru/oplata-u-psixologa-proshla/', url_img='https://memepedia.ru/wp-content/uploads/2024/07/1848935756_0_45_3070_1772_1920x0_80_0_0_7565313e6e5ddce6961fe9422d3d1387-360x270.jpg')
      Meme(title='Дудолить', url='https://memepedia.ru/dudolit/', url_img='https://memepedia.ru/wp-content/uploads/2024/06/dudoling-360x270.jpg')
    
    Memes Words page 2 (15):
      Meme(title='Мёд, медятина', url='https://memepedia.ru/myod-medyatina/', url_img='https://memepedia.ru/wp-content/uploads/2024/05/16049980005faa53701e3a52.98733734-360x270.jpg')
      Meme(title='Чиназес', url='https://memepedia.ru/chinazes/', url_img='https://memepedia.ru/wp-content/uploads/2024/05/chinazes-360x270.jpg')
      Meme(title='Причина тряски', url='https://memepedia.ru/prichina-tryaski/', url_img='https://memepedia.ru/wp-content/uploads/2024/05/prichina-trjaski-memy-360x270.jpg')
      Meme(title='Наш слон', url='https://memepedia.ru/nash-slon/', url_img='https://memepedia.ru/wp-content/uploads/2024/04/nash-slon-360x270.jpg')
      Meme(title='Бобр курва', url='https://memepedia.ru/bobr-kurva/', url_img='https://memepedia.ru/wp-content/uploads/2024/08/bobr4-360x270.jpg')
      Meme(title='Матушка, неужели мы это проглотим', url='https://memepedia.ru/matushka-neuzheli-my-eto-proglotim/', url_img='https://memepedia.ru/wp-content/uploads/2023/07/margarita-simonjan-matushka-360x270.jpg')
      Meme(title='Макеба', url='https://memepedia.ru/makeba/', url_img='https://memepedia.ru/wp-content/uploads/2023/07/screenshot_4-1-360x270.png')
      Meme(title='Я в ахуе. Давайте (Мальчик с “Баунти”)', url='https://memepedia.ru/ya-v-axue-davajte-malchik-s-baunti/', url_img='https://memepedia.ru/wp-content/uploads/2023/04/baunti-360x270.jpg')
      Meme(title='Новиоп', url='https://memepedia.ru/noviop/', url_img='https://memepedia.ru/wp-content/uploads/2023/04/noviob-360x270.jpg')
      Meme(title='Подкрадули', url='https://memepedia.ru/podkraduli/', url_img='https://memepedia.ru/wp-content/uploads/2023/03/podkraduli-mem-360x270.jpg')
      Meme(title='Копиум', url='https://memepedia.ru/kopium/', url_img='https://memepedia.ru/wp-content/uploads/2023/01/kopium-mem-360x270.jpg')
      Meme(title='Вова, ебашь их блять', url='https://memepedia.ru/vova-ebash-ix-blyat/', url_img='https://memepedia.ru/wp-content/uploads/2022/11/screenshot_4-1-360x270.png')
      Meme(title='Гойда', url='https://memepedia.ru/gojda/', url_img='https://memepedia.ru/wp-content/uploads/2022/10/gojda-ohlobystin-360x270.jpg')
      Meme(title='Бавовна', url='https://memepedia.ru/bavovna/', url_img='https://memepedia.ru/wp-content/uploads/2022/08/fz2tfq8xeaeshpk-1-360x270.jpg')
      Meme(title='А мне похуй саншайн', url='https://memepedia.ru/a-mne-poxuj-sanshajn/', url_img='https://memepedia.ru/wp-content/uploads/2022/08/f-vyt-gjeq-cfyifqy-360x270.jpg')
    """
