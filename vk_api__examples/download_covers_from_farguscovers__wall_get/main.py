#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


"""
Получение всех обложек из постов группы https://vk.com/farguscovers
"""


import datetime as DT
import json
import re
import time
import sys

from typing import List, Dict, Generator
from pathlib import Path
from urllib.request import urlretrieve

from vk_api import VkTools


DIR = Path(__file__).resolve().parent

sys.path.append(str(DIR.parent))
from root_common import get_vk_session


DIR_IMAGES = DIR / 'images'
DIR_IMAGES.mkdir(parents=True, exist_ok=True)

FILE_NAME_DUMP = DIR / 'dump.json'


def get_authors(text: str) -> List[Dict[str, str]]:
    return [
        {
            'id': int(user_id),
            'name': user_name,
        }
        for user_id, user_name in re.findall(r'\[id(\d+)\|(.+?)]', text)
    ]


DOMAIN = 'farguscovers'


def get_wall_it() -> Generator:
    vk_session = get_vk_session()
    tools = VkTools(vk_session)

    data = {
        'domain': DOMAIN,
    }
    return tools.get_all_iter('wall.get', 100, data)


if __name__ == '__main__':
    dump = []

    for i, post in enumerate(get_wall_it(), 1):
        post_id = post['id']
        owner_id = post['owner_id']
        post_url = f'https://vk.com/farguscovers?w=wall{owner_id}_{post_id}'

        date_time = DT.datetime.fromtimestamp(post['date'])
        date_time_str = str(date_time)

        post_text = post['text']
        authors = get_authors(post_text)

        try:
            if 'copy_history' in post:
                attachments = post['copy_history'][0].get('attachments', [])
            else:
                attachments = post.get('attachments', [])

            photo_list = [x['photo'] for x in attachments if 'photo' in x]
            if not photo_list:
                continue

            for photo_idx, photo in enumerate(photo_list, 1):
                photo_text = photo['text']
                photo_id = photo['id']

                size = max(photo['sizes'], key=lambda x: (x['height'], x['width']))
                url_raw_photo = size['url']
                photo_post_url = f'https://vk.com/farguscovers?z=photo{owner_id}_{photo_id}%2Fwall{owner_id}_{post_id}'

                print(f'{i} {post_id} {photo_idx} {post_text!r} {photo_text!r} {authors} {url_raw_photo}')

                file_name = DIR_IMAGES / f'{post_id}_{photo_idx}.jpg'
                if not file_name.exists():
                    urlretrieve(url_raw_photo, file_name)
                    time.sleep(2)

                dump.append({
                    'post_id': post_id,
                    'date_time': date_time_str,
                    'post_url': post_url,
                    'post_text': post_text,
                    'photo_file_name': str(file_name.relative_to(DIR)),
                    'photo_post_url': photo_post_url,
                    'authors': authors,
                    'cover_text': '',
                    'game_name': photo_text,  # Часто название игры присутствует к подписи к картинке
                    'game_series': '',        # Будет полезно знать серию игры
                })

        except Exception as e:
            print(i, post_id, post_url, repr(e), post)

        print()

    json.dump(
        dump, open(FILE_NAME_DUMP, 'w', encoding='utf-8'),
        indent=4, ensure_ascii=False
    )
