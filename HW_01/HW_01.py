# Сценарий Foursquare
# Напишите сценарий на языке Python, который предложит пользователю ввести интересующую 
# его категорию(например, кофейни, музеи, парки и т.д.).
# Используйте API Foursquare для поиска заведений в указанной категории.
# Получите название заведения, его адрес и рейтинг для каждого из них.
# Скрипт должен вывести название и адрес и рейтинг каждого заведения в консоль.

import requests
import json
from pprint import pprint
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__),'.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Конечная точка API
endpoint = "https://api.foursquare.com/v3/places/search"

# Определение параметров для запроса
city = input("Введите название города: ")
category = input("Введите название категории: ")
params = {
    "client_id": os.getenv("client_id"),
    "client_secret": os.getenv("client_secret"),
    "near": city,
    "sort": "rating",
    "query": category,
    "limit": 10
}

headers = {
    "Accept": "application/json",
    "Authorization": os.getenv("API_key")
}

# Отправка запроса API и получение ответа
response = requests.get(endpoint, params=params, headers=headers)

# Проверка успешности запроса API
if response.status_code == 200:
    print("Успешный запрос API!")
    data = json.loads(response.text)
    venues = data["results"]
    for venue in venues:
        try:
            print("Название:", venue["name"])
        except:
            print("Название: отсутствует")
        try:
            print("Адрес:", venue["location"]["address"])
        except:
            print("Адрес: отсутствует")
        try:
            print("Рейтинг:", venue["rating"])
        except:
            print("Рейтинг: отсутствует")
        fsq_id = venue["fsq_id"]
        print()
    # pprint(data)
else:
    print("Запрос API завершился неудачей с кодом состояния:", response.status_code)
    print(response.text)

