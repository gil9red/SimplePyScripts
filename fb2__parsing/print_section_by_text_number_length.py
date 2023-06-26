#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from bs4 import BeautifulSoup, Tag


def get_sections_as_dict(root) -> tuple[dict[str, dict], dict[str, Tag]]:
    # Рекурсивная функция поиска <section>
    def _find_sections(root, root_dict: dict, title_by_section: dict):
        for section in root.find_all("section", recursive=False):
            title = section.title.text.strip()
            children = dict()

            root_dict[title] = children
            title_by_section[title] = section

            _find_sections(section, children, title_by_section)

    # Первое <body> должно быть с содержанием, описываемое <section>
    body = root.select_one("body")
    section_by_children = dict()
    title_by_section = dict()

    _find_sections(body, section_by_children, title_by_section)

    return section_by_children, title_by_section


def get_section_by_text(
    section_by_children: dict[str, dict],
    title_by_section: dict[str, Tag],
) -> dict[str, str]:
    def _find_sections(section_by_text, section_by_children):
        for title, children in section_by_children.items():
            if children:
                _find_sections(section_by_text, children)
                continue

            text = title.replace("\n", ". ")
            section = title_by_section[title]

            # Удаление <title>. Тег title относится к section, точнее, оно явлется его названием, поэтому
            # его не нужно включать в текст
            section.title.decompose()

            section_text = section.text.strip()

            section_by_text[text] = section_text

    section_by_text = dict()
    _find_sections(section_by_text, section_by_children)

    return section_by_text


if __name__ == "__main__":
    import glob

    def _print_sections(
        root: dict,
        section_by_text: dict,
        number_length_book_text,
        level=1
    ):
        def _find_section_lines(root, level, lines: list):
            for title, children in root.items():
                text = "{}{}".format("    " * (level - 1), title.replace("\n", ". "))

                if children:
                    text += ":"

                if title in section_by_text:
                    len_num = len(section_by_text[title])

                    lines.append((
                        text,
                        f"{len_num} символов",
                        f"{len_num / number_length_book_text:.2%}",
                    ))
                else:
                    lines.append((text, "", ""))

                _find_section_lines(children, level + 1, lines)

        lines = []

        _find_section_lines(root, level, lines)

        # Список строк станет списком столбцов, у каждого столбца подсчитается максимальная длина
        max_len_columns = [max(map(len, map(str, col))) for col in zip(*lines)]

        # Создание строки форматирования: [30, 14, 5] -> "{:<30} | {:<14} | {:<5}"
        my_table_format = " | ".join("{:<%s}" % max_len for max_len in max_len_columns)

        # Ручное формирование: "{:30} | {:14} | {}"
        # my_table_format = '{:%s} | {:%s} | {}' % (max(len(x[0]) for x in lines), max(len(x[1]) for x in lines))

        for line in lines:
            print(my_table_format.format(*line))

    for fb2_file_name in glob.glob("input/*.fb2"):
        print(fb2_file_name)

        with open(fb2_file_name, encoding="utf-8") as f:
            root = BeautifulSoup(f, "html.parser")

        section_by_children, title_by_section = get_sections_as_dict(root)
        section_by_text = get_section_by_text(section_by_children, title_by_section)

        number_length_book_text = sum(len(text) for text in section_by_text.values())
        print("Всего символов в книге:", number_length_book_text)

        _print_sections(section_by_children, section_by_text, number_length_book_text)

        print("\n")
