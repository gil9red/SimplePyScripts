__author__ = 'ipetrash'


"""Скрипт подсчитывает количество слов в тексте."""


if __name__ == '__main__':
    import re
    from collections import Counter

    text = ("Предоставляет методы для управления дата и значения времени, "
            "связанных с файлом 11 11.")
    words = re.findall(r"\b\w+\b", text)
    print("Words: {}\nCount: {}".format(words, len(words)))
    word_count = Counter(words)
    for word, c in word_count.items():
        print("'{}': {}".format(word, c))