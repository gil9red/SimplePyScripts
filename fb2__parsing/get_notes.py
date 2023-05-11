#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from bs4 import BeautifulSoup
from common import get_attribute_value_by_local_name


def get_note_links(root) -> list[tuple[str, str]]:
    # в стиле Роберта Адама <a l:href="#note1" type="note">[1]</a>
    note_link_list = root.select('a[type="note"]')

    items = []

    for link in note_link_list:
        href = get_attribute_value_by_local_name(link, "href")
        text = link.text.strip()

        items.append((href, text))

    return items


def get_notes(root) -> list[tuple[str, str, str]]:
    # Пример тега:
    # <body name="notes">
    #     <title>
    #         <p>Примечания</p>
    #     </title>
    #     <section id="v1_ch1_cite_note-1">
    #         <title>
    #             <p>1</p>
    #         </title>
    #         <p>Онии-сама: Если кто не знает, это уважительное обращение к старшему брату.
    #     </section>
    notes_list = root.select('body[name="notes"] > section')

    items = []

    for note in notes_list:
        note_id = note.attrs["id"]

        title = note.title.text.strip()

        # Удаление <title>
        note.title.decompose()

        # Теперь можно взять текст -- не попадет заголовок
        text = note.text.strip()

        items.append((note_id, title, text))

    return items


if __name__ == "__main__":
    import glob

    for fb2_file_name in glob.glob("input/*.fb2"):
        with open(fb2_file_name, encoding="utf-8") as f:
            root = BeautifulSoup(f, "html.parser")

        print(fb2_file_name)

        note_links = get_note_links(root)
        print("note_links:", note_links)

        notes = get_notes(root)
        print("notes:", notes)

        print("\n")
