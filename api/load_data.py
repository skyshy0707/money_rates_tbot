"""
Модуль для загрузки данных
"""
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests

from . import config


ERROR_EXTERNAL_API_RESPONSE = JSONResponse(
    status_code=status.HTTP_400_BAD_REQUEST,
    content=jsonable_encoder({ "error": "Невозможно получить данные по этому запросу."})
)

def get_middle_data(url: str, headers: dict=dict(), params: dict=dict()) -> dict:
    """
    Метод, получающий json-данные из внешнего api 
    с учётом обработки возможных исключений
    """
    json = {}
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
        except requests.ConnectionError:
            continue
        else:
            break
    try:
        json = response.json()
    except requests.JSONDecodeError as e:
        json.update({ "error": f"Number: {e.errno if e.errno else 'Unknown number'} - {response.reason}" })
    return json


def get_rate_api_data(response_model: BaseModel) -> dict:
    """
    Метод отправляет запрос пользователя на внешний адрес api 
    курсов валют https://v6.exchangerate-api.com//latest/USD
    и возвращает данные этого api о курсе доллара 
    в эквиваленте к другой валюте или шаблон ответа 
    в случае ошибки.
    """

    exchange_rate_data = get_middle_data(
        config.exchange_rate_api.latest_usd,
    )

    rate_api_data = { "data": exchange_rate_data }

    return response_model(**rate_api_data) if exchange_rate_data else ERROR_EXTERNAL_API_RESPONSE