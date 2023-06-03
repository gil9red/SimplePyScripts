#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install nltk
import nltk

# pip install pymorphy2
import pymorphy2


# TODO: объединить функции is_ADJS_sing_* и is_VERB_sing_*,
#       а проверку пола вынести в отдельую функцию


def is_ADJS_sing_femn(parsed: pymorphy2.analyzer.Parse) -> bool:
    """
    Имя прилагательное (краткое) + единственное число + женский род
    """
    return {"ADJS", "sing", "femn"} in parsed.tag


def is_ADJS_sing_masc(parsed: pymorphy2.analyzer.Parse) -> bool:
    """
    Имя прилагательное (краткое) + единственное число + мужской род
    """
    return {"ADJS", "sing", "masc"} in parsed.tag


def is_VERB_sing_femn(parsed: pymorphy2.analyzer.Parse) -> bool:
    """
    Глагол (личная форма) + единственное число + женский род
    """
    return {"VERB", "sing", "femn"} in parsed.tag


def is_VERB_sing_masc(parsed: pymorphy2.analyzer.Parse) -> bool:
    """
    Глагол (личная форма) + единственное число + мужской род
    """
    return {"VERB", "sing", "masc"} in parsed.tag


def is_NPRO_1per_sing(parsed: pymorphy2.analyzer.Parse) -> bool:
    """
    Местоимение-существительное + 1 лицо + единственное число
    """
    return {"NPRO", "1per", "sing"} in parsed.tag


LOG_DEBUG = False
# LOG_DEBUG = True

morph = pymorphy2.MorphAnalyzer()


def is_femn(text: str) -> bool:
    for line in text.splitlines():
        LOG_DEBUG and print(f"[#] Comment: {line!r}")

        # Перебор предложений
        for sent in nltk.sent_tokenize(line, language="russian"):
            LOG_DEBUG and print(f"[#] Comment part: {sent!r}")

            words = nltk.word_tokenize(sent)
            parsed_words = [morph.parse(word)[0] for word in words]

            parsed = parsed_words[0]
            if is_ADJS_sing_femn(parsed) or is_VERB_sing_femn(parsed):
                return True

            if is_ADJS_sing_masc(parsed) or is_VERB_sing_masc(parsed):
                return False

            has_NPRO_1per_sing = False

            LOG_DEBUG and print(f"[#] ({len(words)}): {words}")
            LOG_DEBUG and print(f"[#] ({len(parsed_words)}):")

            for parsed in parsed_words:
                LOG_DEBUG and print(f"[#]     {parsed.word} - {str(parsed.tag)!r}")

                if is_NPRO_1per_sing(parsed):
                    has_NPRO_1per_sing = True
                    LOG_DEBUG and print(f'[!]{" " * 12} FOUND #1!')
                    continue

                if has_NPRO_1per_sing:
                    # Если встретили в мужском роде, выходим
                    if is_ADJS_sing_masc(parsed) or is_VERB_sing_masc(parsed):
                        return False

                    if is_ADJS_sing_femn(parsed) or is_VERB_sing_femn(parsed):
                        LOG_DEBUG and print(f'[!]{" " * 12} FOUND #2!')
                        return True

    return False


if __name__ == "__main__":
    import json

    with open("comments.json", encoding="utf-8") as f:
        data = json.load(f)

    comments = [(x["text"], x["expected"]) for x in data]

    matches = 0
    total = len(comments)

    for i, (text, expected) in enumerate(comments, 1):
        has_female = is_femn(text)
        match = has_female == (expected == "female")
        matches += match

        print(
            f"{i}. {text!r}"
            f"\n    [{'+' if match else '-'}] "
            f"Expected={expected}, "
            f"actual={'female' if has_female else 'male'}"
        )
        print("-" * 100)

    print(f"Total: {matches} / {total}")
