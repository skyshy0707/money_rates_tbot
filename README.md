Приложение на Python 3.8 для автоматических сообщений о курсе доллара в чате 
`money_rates_tbot`[https://t.me/currency_unit_rates_bot] по последним данным 
api https://v6.exchangerate-api.com/v6

Позволяет в чате бота `money_rates_tbot` получать данные о текущем курсе доллара в 
российских рублях.


**Команды**

*Запуск/Приветствие бота:*

```
/start
```

*Получить данные о текущем курсе доллара в рублях:*

```
<Ответьте боту, написав ваше имя>
```


!NB Настройки:

При необходимости, в файле `/api/config.py` -- в переменной `exchange_rate_api.base_url` 
вида https://v6.exchangerate-api.com/v6/API_KEY поменяйте `API_KEY` на свой*

*Получить `API_KEY` можно при регистрации личного кабинета в сервисе:
[ExchangeRate-API](https://app.exchangerate-api.com/sign-up), используя свой email.


Создайте бота в телеграмм, используя [чат конструктора](https://t.me/BotFather)
Получите токен доступа к боту через HTTP API
Измените значение токена доступа бота `BOT_TOKEN` в `bot/congig.py`

**Запуск проекта**


*Сборка:*

```
docker-compose up -d --build

```

*Поднять контейнеры:*
```
docker-compose up
```