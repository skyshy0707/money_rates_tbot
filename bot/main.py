import os
import sys
import telebot
from telebot import types

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from api import load_data
from bot import config, templates

bot = telebot.TeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_bot(message: types.Message):
    """
    Стартовое справочное сообщение
    """
    first_message = templates.start_message

    sended_message = bot.send_message(
        message.chat.id, first_message, parse_mode="html"
    )
    bot.register_next_step_handler(sended_message, currency_rate)

@bot.message_handler(content_types=['text'])
def users_answer(message: types.Message):
    """
    Отправляет регулярные сообщения о курсе валюты на ответ в беседе
    """
    currency_rate(message)

def currency_rate(message: types.Message):
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

    erate_data = load_data.get_middle_data(
        f"{config.EXCHANGE_RATE_DATA_URL}/latest/{target_unit}"
    )

    if erate_data.get("error"):
        response_message = templates.error_erate_api_message\
            .format(**erate_data)

    else: 
        response_message = templates.erate_message\
            .format(
                username=message.text,
                target_unit=target_unit,
                unit_value=erate_data["data"].get(target_unit)
            )
        
    bot.send_message(
        message.chat.id, text=response_message, parse_mode="html"
    )


bot.infinity_polling()
