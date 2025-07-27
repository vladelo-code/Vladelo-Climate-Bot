import requests
from bs4 import BeautifulSoup
import re


# Функция для парсинга данных с сайта @Погода
def get_weather_data(city: str, month: int):
    # Собираем URL и делаем get запрос
    url = f'https://pogoda.mail.ru/prognoz/{city}/by-month/'
    response = requests.get(url)

    # Проверяем код запроса
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'lxml')

    # Вытаскиваем из кода страницы нужные участки с температурами и влажностью
    temperatures_code = soup.find_all('div', 'day__temperature')
    humidity_code = soup.find_all('div', 'day__additional-group')

    # Компилируем регулярные выражения для поиска
    regex_temperature = re.compile(r'>([-+0-9]+)°')
    regex_humidity = re.compile(r'>([0-9]+)%')

    # Заносим в список нужные данные: температуры и влажность
    temperatures_list = re.findall(regex_temperature, str(temperatures_code[month - 1]))
    humidity_list = re.findall(regex_humidity, str(humidity_code[month - 1]))

    # Проверяем, что регулярные выражения отработали корректно и присваиваем переменным соответствующие значения
    if temperatures_list and humidity_list:
        temp_day, temp_night = temperatures_list[0], temperatures_list[1]
        humidity = humidity_list[0]
    else:
        return None

    # Формируем словарь для return-a в bot.py
    return {
        "temp_day": temp_day,
        "temp_night": temp_night,
        "humidity": humidity
    }
