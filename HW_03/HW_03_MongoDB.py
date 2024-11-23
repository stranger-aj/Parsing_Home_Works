# Установите MongoDB на локальной машине, а также зарегистрируйтесь в онлайн-сервисе.
# https: // www.mongodb.com / https: // www.mongodb.com/products/compass

import json
from pymongo import MongoClient
from pymongo.errors import *

# Загрузите данные который вы получили на предыдущем уроке путем скрейпинга сайта с помощью Buautiful Soup
# в MongoDB и создайте базу данных и коллекции для их хранения.
client = MongoClient('mongodb://localhost:27017/')
db = client["books_store_base"]
collection = db["books"]

collection.delete_many({})

with open('HW_03\my_books_file.json', 'r') as file:
    file_data = json.load(file)

for book in file_data['book_info']:
    try:
        collection.insert_one(book)
    except DuplicateKeyError as e:
        print("Обнаружен дубликат")

# # Поэкспериментируйте с различными методами запросов.
count = collection.count_documents({})
print(f'Число записей в базе данных: {count}')

for book in collection.find({'count in stock': {"$lt": 2}}):
    print(book['name'])

for book in collection.find({'description': {'$regex': 'bestseller'}}):
    print(book['name'])

for book in collection.find({'name': 'The Communist Manifesto'}):
    print(book['price(euro)'])
    new_price = input('введите новую стоимость : ')
    collection.update_one({'name': 'The Communist Manifesto'}, {
                          '$set': {'price(euro)': new_price}})

collection.delete_one(
    {'name': input('введите название книги для удаления : ')})
