import asyncio
import os
import sys
import telebot
from telebot import types
from telebot.asyncio_filters import StateFilter


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from api import load_data
from bot import config, templates
from bot.states import State

bot = telebot.TeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_bot(message: types.Message):
    """
    Стартовое справочное сообщение
    """
    first_message = templates.start_message
    bot.send_message(message.chat.id, first_message, parse_mode="html")
    bot.set_state(State.ANS_YOUR_NAME, message.chat.id)


@bot.message_handler(StateFilter(State.ANS_YOUR_NAME))
async def ans_your_name(message: types.Message):
    """
    Обработчик ответа пользователя на вопрос `Как твоё имя?`
    """
    your_chat = message.chat.id
    if message.text:
        await bot.storage.set_data(message.text, your_chat)
        await currency_rate(message)

        bot.finish_state(your_chat)
        bot.register_next_step_handler(message, next_text)


async def next_text(message: types.Message):
    """
    Обработчик произвольного текста от пользователя для регулярных 
    сообщений бота /Когда ответ от пользователя был уже получен/
    """
    await currency_rate(message)

async def currency_rate(message: types.Message):
    """
    Функция, формумирующая экземпляр сообщения
    о курсе доллара в рублях по последним данным внешнего api
    https://www.exchangerate-api.com

    Эту функцию можно переписать на другую валюту, описанную 
    в https://www.exchangerate-api.com/docs/supported-currencies, 
    изменив в ней локальную переменную `target_unit`. Пока что, задача 
    стояла для курса доллара в рублях (RUB).
    """
    target_unit = "RUB"
    name = await bot.get_data(chat=message.chat.id)

    if not name:
        return

    erate_data = await load_data.get_middle_data(
        f"{config.EXCHANGE_RATE_DATA_URL}/latest/{target_unit}"
    )

    if erate_data.get("error"):
        response_message = templates.error_erate_api_message\
            .format(**erate_data)

    else: 
        response_message = templates.erate_message\
            .format(
                username=name,
                target_unit=target_unit,
                unit_value=erate_data["data"].get(target_unit)
            )
        
    bot.send_message(
        message.chat.id, text=response_message, parse_mode="html"
    )


if __name__ == "__main__":
    asyncio.run(bot.infinity_polling())