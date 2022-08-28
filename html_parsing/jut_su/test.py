#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
import unittest

import get_possible_achievements
import get_user_achievements

from search import search


class GetPossibleAchievementsTestCase(unittest.TestCase):
    def test_parse_this_anime_achievement(self):
        text = """
        category: "events",
        time_start: 704,
        title: "Ядовитый бутон",
        description: "Высвобождение Заэльаппоро",
        icon: js_preres_url + "/uploads/achievements/icons/5703.jpg",
        id: "5703",
        hash: "11560c9068571116"
        """
        actual = get_possible_achievements.parse_this_anime_achievement(text)
        expected = {
            'category': 'events',
            'time_start': '704',
            'title': 'Ядовитый бутон',
            'description': 'Высвобождение Заэльаппоро',
            'icon': 'js_preres_url + "/uploads/achievements/icons/5703.jpg"',
            'id': '5703',
            'hash': '11560c9068571116'
        }
        self.assertEqual(actual, expected)

    def test_parse_this_anime_achievements(self):
        text = """
        var this_anime_achievements = [];
        this_anime_achievements.push({
        category: "events",
        time_start: 704,
        title: "Ядовитый бутон",
        description: "Высвобождение Заэльаппоро",
        icon: js_preres_url + "/uploads/achievements/icons/5703.jpg",
        id: "5703",
        hash: "11560c9068571116"
        });
        this_anime_achievements.push({
        category: "events",
        time_start: 1286,
        title: "Не изменилась",
        description: "Нелл не думает сдаваться",
        icon: js_preres_url + "/uploads/achievements/icons/5704.jpg",
        id: "5704",
        hash: "dc3acd1d8af21525"
        });
        """
        actual = get_possible_achievements.parse_this_anime_achievements(text)
        expected = [
            {
                'category': 'events',
                'time_start': '704',
                'title': 'Ядовитый бутон',
                'description': 'Высвобождение Заэльаппоро',
                'icon': 'js_preres_url + "/uploads/achievements/icons/5703.jpg"',
                'id': '5703',
                'hash': '11560c9068571116'
            },
            {
                'category': 'events',
                'time_start': '1286',
                'title': 'Не изменилась',
                'description': 'Нелл не думает сдаваться',
                'icon': 'js_preres_url + "/uploads/achievements/icons/5704.jpg"',
                'id': '5704',
                'hash': 'dc3acd1d8af21525'
            }
        ]
        self.assertEqual(actual, expected)

    def test_get_achievements(self):
        actual = get_possible_achievements.get_achievements('https://jut.su/bleeach/episode-193.html')
        self.assertTrue(actual)

        expected = [
            {
                'category': 'events',
                'time_start': '704',
                'title': 'Ядовитый бутон',
                'description': 'Высвобождение Заэльаппоро',
                'icon': 'js_preres_url + "/uploads/achievements/icons/5703.jpg"',
                'id': '5703',
                # 'hash': '11560c9068571116'
            },
            {
                'category': 'events',
                'time_start': '1286',
                'title': 'Не изменилась',
                'description': 'Нелл не думает сдаваться',
                'icon': 'js_preres_url + "/uploads/achievements/icons/5704.jpg"',
                'id': '5704',
                # 'hash': 'dc3acd1d8af21525'
            }
        ]

        # Хеш может отличаться (думаю, от пользователя к пользователю), поэтому нужно убрать его
        for achievement in actual:
            achievement.pop('hash')

        self.assertEqual(actual, expected)


class GetUserAchievementsTestCase(unittest.TestCase):
    def test_get_achievements(self):
        url = 'https://jut.su/user/gil9red/achievements/'

        get_achievements = get_user_achievements.get_achievements

        items_1_50 = get_achievements(url, need_total_items=50)
        time.sleep(1)  # Задержка перед следующим запросом

        items_1_1 = get_achievements(url, need_total_items=1)
        time.sleep(1)

        with self.subTest(msg='Проверка reversed'):
            expected = get_achievements(url, reversed=False, need_total_items=50)
            self.assertEqual(items_1_50, expected)

        time.sleep(1)

        with self.subTest(msg='Проверка need_total_items'):
            self.assertTrue(1, len(items_1_1))

            items_1_51 = get_achievements(url, need_total_items=51)
            self.assertTrue(51, len(items_1_51))

        time.sleep(1)

        with self.subTest(msg='Проверка start_page=1'):
            self.assertEqual(
                items_1_1,
                get_achievements(url, start_page=1, need_total_items=1),
            )

        time.sleep(1)

        with self.subTest(msg='Проверка start_page и need_total_items'):
            self.assertTrue(50, len(items_1_50))

            items_2_50 = get_achievements(url, start_page=2, need_total_items=50)
            self.assertTrue(50, len(items_2_50))

            time.sleep(1)

            items_1_100 = get_achievements(url, need_total_items=100)
            self.assertTrue(100, len(items_1_100))

            self.assertEqual(items_1_50 + items_2_50, items_1_100)

        time.sleep(1)

        with self.subTest(msg='Проверка reversed=True'):
            items_1_50_reversed = get_achievements(url, need_total_items=50, reversed=True)
            expected = items_1_50_reversed[::-1]
            self.assertEqual(items_1_50, expected)


class SearchTestCase(unittest.TestCase):
    def test_search(self):
        self.assertFalse(search(text='21331231ваываыва'))

        self.assertTrue(search(text='bleach'))

        text = 'Чёрный'
        items = [x.title for x in search(text=text)]
        self.assertTrue(
            any(text in title for title in items),
            f'{text!r} не найден в {items}'
        )


if __name__ == '__main__':
    unittest.main()
