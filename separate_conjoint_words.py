__author__ = "ipetrash"


def separate_conjoint_words(text):
    """Функция разделяет слитные слова, на пересечении разных регистров или при встрече с цифрой и оформляет строку
    в виде предложения: первый символ заглавный, остальные строчные.
    Пример: CardsPickedSinceCleaningCard -> Cards picked since cleaning card
            TotalPickedInputHopper6      -> Total picked input hopper 6
    """
    if not text:
        return text

    res = ""
    for c in text:
        res += " " + c if c.isupper() or c.isdigit() else c

    # Удаление пробелов с краев
    res = res.strip()

    # Первый символ в верхний регистр, остальные в нижний
    return res.capitalize()


if __name__ == "__main__":
    print(separate_conjoint_words("helloWorld!"))
    print(separate_conjoint_words("DogLike1234"))
