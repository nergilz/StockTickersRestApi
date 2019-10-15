
## REST-API Сервис контроля цен по биржевым котировкам

+ Сервис позволяет подписываться на изменения по биржевым котировкам. 
+ Сервис предоставлять _HTTP API_ для контроля подписки по запросу
+ Данные в формате _JSON_
+ Для получения информации о котировках используется API [alphavantage](https://www.alphavantage.co)
+ При привышении лимита по подписке на почту приходит уведомление вида: 
  _Warning in <TICKER> In Ticker "symbol" >< max or min price_

### Создание подписки на уведомления по тикеру:
- `email`     - _email_ для подписки на уведомления 
- `symbol`    - код акции или инструмента
- `max_price` - если цена на _ticker_ поднимется выше этого значения, на _email_ отправлено уведомление
- `min_price` - если цена _ticker_ опустится ниже этого значения, на _email_ отправлено уведомление

### Требования (requirements)
+ [virtualenv](https://virtualenv.pypa.io/en/latest/)
+ [Python 3.7](https://www.python.org/)
+ [pip3](https://pip.pypa.io/en/latest/installing/)
+ [Django2](https://docs.djangoproject.com)
+ [Django-rest-framework](https://www.django-rest-framework.org/)
+ [Djoser](https://djoser.readthedocs.io/en/latest/getting_started.html)
+ [Celery](https://docs.celeryproject.org/en/latest/)
+ [Redis](https://redis.io/)
+ [curl](https://curl.haxx.se/docs/httpscripting.html) Для проверки rest-api

### Установка зависимостей
```bash
(venv)name@host:~/poject/ pip3 install -r requirements.txt
```
```bash
$ sudo apt install redis-server
```

### запуск сервиса
```bash
name@host:~/ sudo service redis-server start
``` 
```bash
(venv)name@host:~/poject/ ./manage runserver 8080 
```
```bash
(venv)name@host:~/poject/ celery -A tickers_api_v2 worker -B -l INFO
```

#### получить токен
```bash
$ curl -X POST http://localhost:8080/api/v2/authtoken/token/login/ --data "username=user1&password=user1user1"
```
```bash
{"auth_token":"e06f996da2cace8bd0edff5ffb499ad3f11a67bd"}
```

#### подписка на тикер по токену
```bash
$ curl -X POST http://localhost:8080/api/v2/tickers/create/ -H "Content-Type: application/json" -H "Authorization: Token e06f996da2cace8bd0edff5ffb499ad3f11a67bd" -d '{"symbol":"DELL", "max_price":"51.00", "min_price":"50.01", "email":"qarixq@yandex.ru"}'
```

#### получение данных
```bash
$ curl -LX GET http://localhost:8000/api/v2/tickers/all/ -H "Authorization: Token e06f996da2cace8bd0edff5ffb499ad3f11a67bd"
```
```bash
[{"id":1,"user":"admin","symbol":"AAPL"},{"id":2,"user":"user1","symbol":"TSM"},{"id":3,"user":"user1","symbol":"INTC"},{"id":4,"user":"user2","symbol":"CSCO"},{"id":5,"user":"user2","symbol":"IBM"},{"id":6,"user":"user1","symbol":"NVDA"},{"id":7,"user":"user1","symbol":"ASML"}]
```

#### Удаление тикера по ID
```bash
$ curl -X DELETE http://127.0.0.1:8080/api/v2/tickers/detail/<ID>/ -H "Authorization: Token e06f996da2cace8bd0edff5ffb499ad3f11a67bd"
```

### API endpoints
```bash
http://localhost:8080/api/v2/tickers/all/
http://localhost:8080/api/v2/tickers/create/
http://localhost:8080/api/v2/tickers/detail/<int>/
http://localhost:8080/api/v2/authtoken/token/login/
http://localhost:8080/api/v2/authtoken/token/logout/
```

### Изменить конфигурации хоста для отправки сообщений
```bash
tickers_api_v2/settings.py
```
```python
EMAIL_USE_TLS = True
EMAIL_HOST = "<your@email.com>"
EMAIL_PORT = 587
EMAIL_HOST_USER = "<login>"
EMAIL_HOST_PASSWORD = "<password>"
```

---
##### для проверки:
+ admin :  _admin_:_admin_ 
+ user  :  _user1_:_user1user1_ 

---

This code is written as a test for [KODE](https://kode.ru/) company.
