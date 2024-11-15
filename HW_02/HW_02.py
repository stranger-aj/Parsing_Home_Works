
# Выполнить скрейпинг данных в веб-сайта 
# http: // books.toscrape.com / и извлечь информацию о всех книгах на сайте во всех категориях: 
# название, цену, количество товара в наличии(In stock(19 available)) в формате integer, описание.
# Затем сохранить эту информацию в JSON-файле.

import requests
import json
import re
import pandas as pd
from pprint import pprint
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
url_base = 'http://books.toscrape.com'
url_temp = 'http://books.toscrape.com/catalogue/'
url = 'http://books.toscrape.com'
headers = {"User-Agent": ua.random}
session = requests.session()
book_info = []
num_page = 1

while True:
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('li', ('class', 'col-xs-6'))
    print('page = ', num_page)

    for row in rows:
        book = {}
        # получение названия книги\
        try:
            name_info = row.find('h3').find('a')
            book['name'] = name_info['title']
        except:
            book['name'] = None
        # получение стоимости книги
        try:
            price_info = row.find('p', ('class', 'price_color'))
            price_text = price_info.getText()
            book['price(euro)'] = float('.'.join(re.findall(r'\d+', price_text)))
        except:
            book['price(euro)'] = None
        # переход по ссылке на конкретную книгу
        try:
            stock_info = row.find('div', ('class', 'image_container')).find('a')
            if num_page == 1 :
                link_into = session.get(
                    url_base + "/" + stock_info['href'], headers=headers)
            else:
                link_into = session.get(
                    url_base + "/catalogue/" + stock_info['href'], headers=headers)
            soup_2 = BeautifulSoup(link_into.text, 'html.parser')
        except:
            book['count in stock'] = None
            book['description'] = None
            continue
        # получение информации о наличии
        try:
            count_text = soup_2.find('p', ('class', 'instock availability')).getText()
            book['count in stock'] = int(''.join(filter(str.isdigit, count_text)))
        except:
            book['count in stock'] = None
        # получение описания книги
        try:
            description_info = soup_2.find('div', ('class', 'sub-header')).find_next_sibling().getText()
            book['description'] = description_info
        except:
            book['description'] = None
        book_info.append(book)
    try:
        next_page_link = soup.find('li', ('class', 'next')).find('a')
    except:
        break
    next_page_link = next_page_link['href'][next_page_link['href'].index('page'):]
    url = url_temp + next_page_link
    num_page += 1
    
    
df = pd.DataFrame(book_info)
df.to_json('books_file.json', orient='records', lines=True)
