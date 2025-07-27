from transliterate import translit

# Словарь с месяцами для перевода
MONTHS = {
    "январь": 1, "февраль": 2, "март": 3, "апрель": 4,
    "май": 5, "июнь": 6, "июль": 7, "август": 8,
    "сентябрь": 9, "октябрь": 10, "ноябрь": 11, "декабрь": 12
}

# Словарь с популярными исключениями городов, чтобы парсер работал корректно
EXCEPTIONS = {'питер': 'sankt_peterburg',
              'санкт-петербург': 'sankt_peterburg',
              'санкт петербург': 'sankt_peterburg',
              'великий новгород': 'novgorod',
              'белград': 'belgrade',
              }


# Функция для перевода названия города в транслит
def city_to_translit(city_name: str) -> str:
    try:
        # Пытаемся найти этот город в исключениях, иначе – просто переводим в транслит
        return EXCEPTIONS[city_name]
    except KeyError:
        # Переводим в транслит
        result = translit(city_name, 'ru', reversed=True).lower()

        # Исправляем неточности транслита
        result = result.replace('ij', 'iy').replace('yj', 'yy').replace('ja', 'ya').replace('jo', 'yo')
        result = result.replace(' ', '_').replace('\'', '')

        return result


# Функция для перевода названия месяца в число
def month_to_number(month_name: str) -> int:
    return MONTHS.get(month_name, None)
