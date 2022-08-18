#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import unittest

from search import search
from get_possible_achievements import parse_this_anime_achievement, parse_this_anime_achievements, get_achievements


# TODO: Добавить тесты других скриптов


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
        actual = parse_this_anime_achievement(text)
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
        actual = parse_this_anime_achievements(text)
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
        actual = get_achievements('https://jut.su/bleeach/episode-193.html')
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
