# Зарегистрируйтесь в ClickHouse.
# Загрузите данные в ClickHouse и создайте таблицу для их хранения.
from clickhouse_driver import Client
import json

client = Client('localhost')
client.execute('CREATE DATABASE IF NOT EXISTS book_store')

with open('HW_03\my_books_file.json', 'r') as file:
    file_data = json.load(file)

data = file_data['book_info']

client.execute('''
CREATE TABLE IF NOT EXISTS book_store.books (
    name String,
    price Float64,
    count_in_stock UInt64,
    description String
) ENGINE = MergeTree()
ORDER BY name
''')
print("Таблица создана успешно.")


for book in data:
    client.execute("""INSERT INTO book_store.books (name, price, count_in_stock, description) VALUES""",
    [(book['name'] or "", 
    book['price(euro)'], 
    book['count in stock'], 
    book['description'] or "")])

print("Данные введены успешно.")

# Проверка успешности вставки
result = client.execute("SELECT * FROM book_store.books")
print("Вставленная запись:", result[0])
