#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List, Tuple
from generate_dataset_for_labeled import get_dataset_text


def generate(file_name_to: str, links: List[Tuple[str, str]], title="Graph"):
    template_title = '{{title}}'
    template_dataset = '{{dataset}}'

    dataset_text = get_dataset_text(links)

    with open('template_graph.html', 'r', encoding='utf-8') as f:
        text = f.read()
        text = text.replace(template_title, title)
        text = text.replace(template_dataset, dataset_text)

    with open(file_name_to, 'w', encoding='utf-8') as f:
        f.write(text)


if __name__ == '__main__':
    links = [('Adam', 'Bob'), ('Adam', 'Ivan'), ('Bob', 'Iris'), ('Bob', 'Jerry'), ('Iris', 'George')]
    generate('example.html', links)

    links = [('Сквайр', 'Рыцарь'), ('Сквайр', 'Охотник на ведьм'), ('Охотник на ведьм', 'Инквизитор'), ('Инквизитор', 'Великий инквизитор'), ('Рыцарь', 'Рыцарь Империи'), ('Рыцарь Империи', 'Ангел'), ('Рыцарь Империи', 'Паладин'), ('Паладин', 'Святой мститель'), ('Паладин', 'Защитник веры')]
    generate('example_disciples.html', links, title='Graph Disciples')
