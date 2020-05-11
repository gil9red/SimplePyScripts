#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import base64
from dataclasses import dataclass
from urllib.parse import urlsplit, urljoin
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup
import requests


URL = 'https://kanobu.ru/games/collections/igry-s-podderzhkoi-rtx/'


@dataclass
class Game:
    title: str
    url: str
    img_base64: str

    def as_html_card(self) -> str:
        # SOURCE: https://www.w3schools.com/howto/howto_css_cards.asp
        return f"""
            <div class="card" title="{self.title}">
                <img src="{self.img_base64}" alt="{self.title}" style="width:100%">
                <div class="container">
                    <h4 class="truncate"><b><a href="{self.url}">{self.title}</a></b></h4>
                </div>
            </div>
        """


def img_to_base64_html(rs: requests.Response) -> str:
    path = urlsplit(rs.url).path
    suffix = Path(path).suffix.lower()[1:]

    img_base64 = base64.b64encode(rs.content).decode('utf-8')
    return f'data:image/{suffix};base64,{img_base64}'


def get_games() -> List[Game]:
    session = requests.session()
    rs = session.get(URL)
    root = BeautifulSoup(rs.content, 'html.parser')

    items = []

    for game in root.select('li.c-game a.c-game__img'):
        url_game = urljoin(rs.url, game['href'])

        img = game.img
        title = img['title']
        url_img = img.get('data-original') or img.get('src')
        rs_img = session.get(url_img)
        img_base64 = img_to_base64_html(rs_img)

        items.append(
            Game(title, url_game, img_base64)
        )

    return items


def save_as_html(file_name: str, items: List[Game], columns=4):
    title = 'Games with RTX'

    with open(file_name, 'w', encoding='utf-8') as f:
        # SOURCE: https://www.w3schools.com/howto/howto_css_cards.asp
        f.write("""
            <html lang="ru">
            <head>
                <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
                <title>{{ title }}</title>
                <style>
                    .card {
                        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.5);
                        transition: 0.3s;
                        border-radius: 5px; /* 5px rounded corners */
                        width: 220px
                    }
                    
                    /* On mouse-over, add a deeper shadow */
                    .card:hover {
                        box-shadow: 0 8px 16px 0 rgba(0,0,0,1);
                    }
                    
                    /* Add rounded corners to the top left and the top right corner of the image */
                    img {
                        border-radius: 5px 5px 0 0;
                        width: 200px;
                        height: 300px;
                    }
                    
                    /* Add some padding inside the card container */
                    .container {
                        padding: 5px;
                    }
                    .truncate {
                        white-space: nowrap; /* Запрещаем перенос строк */
                        overflow: hidden; /* Обрезаем все, что не помещается в область */
                        text-overflow: ellipsis; /* Добавляем многоточие */
                    }
    
                </style>
            </head>
            <body>
                <div style="width: 800px; margin:0 auto;">
                    <h1><a href="{{ URL }}">{{ title }}</a></h1>
                    <table cellspacing="5">
        """.replace('{{ title }}', title).replace('{{ URL }}', URL))

        for i in range(0, len(items), columns):
            f.write("<tr>")

            for game in items[i: i+columns]:
                f.write(f"<td>{game.as_html_card()}</td>")

            f.write("</tr>")

        f.write("""
                    </table>
                </div>
            </body>
            </html>
        """)


if __name__ == '__main__':
    items = get_games()
    print(f'Games ({len(items)}):')
    for i, x in enumerate(items, 1):
        print(f'    {i:2}: {x.title!r}')
    # Games (26):
    #      1: 'Minecraft'
    #      2: 'Cyberpunk 2077'
    #      3: 'Metro: Exodus'
    # ...
    #     25: 'Fractured Lands'
    #     26: 'Synced: Off Planet'

    print()

    file_name = str(Path(__file__).resolve()) + '.html'
    print('Save as HTML:', file_name)
    save_as_html(file_name, items)
