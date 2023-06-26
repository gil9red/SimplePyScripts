__author__ = "ipetrash"


def mils2mm(mils: float) -> float:
    """Функция конвертирует mils (1/1000 дюйма) в mm (миллиметры)."""

    mm = (mils / 1000) * 25.4
    return round(mm, 2)


def mm2mils(mm: float) -> float:
    """Функция конвертирует mm (миллиметры) в mils (1/1000 дюйма)."""

    mils = (mm * 1000) / 25.4
    return round(mils, 2)


if __name__ == "__main__":
    mm = 50.0
    mils = 1968.0
    print(f"{mm} mm -> {mm2mils(mm)} mils")
    print(f"{mils} mils -> {mils2mm(mils)} mm")
