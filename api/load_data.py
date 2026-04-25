"""
Модуль для загрузки данных
"""
import aiohttp
import asyncio
import json

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from api import config


ERROR_EXTERNAL_API_RESPONSE = JSONResponse(
    status_code=status.HTTP_400_BAD_REQUEST,
    content=jsonable_encoder({ "error": "Невозможно получить данные по этому запросу."})
)

async def get_middle_data(url: str, headers: dict=dict(), params: dict=dict()) -> dict:
    """
    Метод, получающий json-данные из внешнего api 
    с учётом обработки возможных исключений
    """
    json_data = {}

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(url, headers=headers, params=params) as response:
                    try:
                        json_data = await response.json()
                    except json.JSONDecoderError as e:
                        json_data.update({ "error": f"Number: {e.errno if e.errno else 'Unknown number'} - {response.reason}" })
                        break
            except aiohttp.ClientError as e:
                json_data.update({ "error": "Number: Client Error" })
                break

            except aiohttp.ConnectionTimeoutError:
                await asyncio.sleep(18)
            else:
                break
    return json_data


async def get_rate_api_data(response_model: BaseModel) -> dict:
    """
    Метод отправляет запрос пользователя на внешний адрес api 
    курсов валют https://v6.exchangerate-api.com//latest/USD
    и возвращает данные этого api о курсе доллара 
    в эквиваленте к другой валюте или шаблон ответа 
    в случае ошибки.
    """

    exchange_rate_data = await get_middle_data(
        config.exchange_rate_api.latest_usd,
    )

    rate_api_data = { "data": exchange_rate_data }

    return response_model(**rate_api_data) if exchange_rate_data else ERROR_EXTERNAL_API_RESPONSE