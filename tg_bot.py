import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from utils import city_to_translit, month_to_number
from parser import get_weather_data
from config import BOT_TOKEN

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Обрабатываем команду /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        'Привет! 🤟🏻\nЭто Vladelo-Climate-Bot, я подскажу тебе погоду в нужном городе за указанный месяц.\nПросто отправь мне город и месяц.\n\n<b>Формат ввода:</b>\n<i>Москва</i>\n<i>Март</i>',
        parse_mode='HTML')


# Обрабатываем команду /how
@dp.message(Command('how'))
async def start(message: Message):
    await message.answer('Тут будет описание проекта.', parse_mode='HTML')


# Обрабатываем команду /help
@dp.message(Command('help'))
async def start(message: Message):
    await message.answer('Если у тебя возникли вопросы или сложности, пишите мне @vladelo.')


# Обрабатываем введенные данные
@dp.message()
async def process_message(message: Message):
    try:
        # Разделяем введенные данные по '\n' и присваиваем в переменные city и month
        city, month = message.text.split('\n')

        # Убираем пробелы по краям и приводим month к нижнему регистру
        city, month = city.strip(), month.strip().lower()

        # Переводим название города в транслит и выводим в лог
        city_translit = city_to_translit(city.lower())
        logging.info(f'Преобразование города: {city} -> {city_translit}')

        # Переводим название месяца в число и выводим в лог
        month_number = month_to_number(month)
        logging.info(f'Преобразование месяца: {month} -> {month_number}')

        # Если месяц не удалось перевести, то выводим сообщение об ошибке
        if not month_number:
            await message.answer("Ошибка! Введите корректный месяц.")
            return None

        # Обращаемся к парсеру и получаем словарь с данными для вывода в бот
        weather_data = get_weather_data(city_translit, month_number)

        # Проверяем, что словарь не пустой и выводим данные, иначе – сообщение об ошибке
        if weather_data:
            response = (f"Погода в городе {city} за {month}:\n"
                        f"🌞 Днем: {weather_data['temp_day']}°C\n"
                        f"🌙 Ночью: {weather_data['temp_night']}°C\n"
                        f"💧 Влажность: {weather_data['humidity']}%")
        else:
            response = "Не удалось получить данные о погоде.\nВозможно, такого города не существует или по нему отсутствуют данные о погоде."

    except ValueError:
        response = "Ошибка! Введите город и месяц в указанном формате:\n<i>Москва</i>\n<i>Март</i>"

    # Отправляем ответ пользователю
    await message.answer(response, parse_mode='HTML')


# Функция для запуска бота, её мы вызываем из main.py
async def main():
    await dp.start_polling(bot)
