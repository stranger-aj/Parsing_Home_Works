# Выберите веб-сайт с табличными данными, который вас интересует.
# Напишите код Python, использующий библиотеку requests для отправки HTTP GET-запроса на
# сайт и получения HTML-содержимого страницы.
# Выполните парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные из таблицы.
# Сохраните извлеченные данные в CSV-файл с помощью модуля csv.
# Ваш код должен включать следующее:
# Строку агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер и избежать
# блокировки сервером.
# Выражения XPath для выбора элементов данных таблицы и извлечения их содержимого.
# Обработка ошибок для случаев, когда данные не имеют ожидаемого формата.
# Комментарии для объяснения цели и логики кода.

import requests
from lxml import html
import csv

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

# основная ссылка на сайт news.mail.ru (был рекомендован на семинаре)
url = 'https://news.mail.ru/'
# запрос к разделу экономических новостей
response = requests.get(url + 'economics/', headers=header)
print(response.status_code)
news = html.fromstring(response.text)

i = 0
# список ссылок на новости
items_list = []
# список для словарей с извлекаемывми данными
eco_news_list = []

# получение ссылок на новости
items = news.xpath(
    "//div[contains(@class, 'cols__inner')]//a[contains(@class, 'link')]")
for item in items[1:]:
    url_of_eco_news = item.xpath("./@href")[0]
    items_list.append(url_of_eco_news)

# формирование базы новостей (ссылка, название, источник, контент)
for url_of_eco_news in items_list:
    data = {}
    response_eco_news = requests.get(url_of_eco_news, headers=header)
    # проверка корректности ссылки
    if response_eco_news.status_code == 200:
        news_eco = html.fromstring(response_eco_news.text)
        data['link'] = url_of_eco_news
        try:
            name = news_eco.xpath("//h1[@data-qa = 'Title']/text()")[0]
            data['name'] = name
        except:
            data['name'] = None
        try:
            sourse = news_eco.xpath("//div[@aria-label = 'Навигация']//a/text()")[0]
            data['sourse']= sourse
        except:
            data['sourse']= None
        try:
            article = news_eco.xpath("//section[@data-qa= 'Article']")[0]
            content = article.xpath("//div[@article-item-type = 'html']/div/p/text()")
            content.extend(article.xpath("//div[@article-item-type = 'html']/div/descendant::span/text()"))
            # очистка и объединение блоков текста статьи
            data['content'] = ' '.join(' '.join(content).split())
        except:
            data['content'] = None
        # формирование списка данных
        eco_news_list.append(data)

# запись в файл news.csv
keys = eco_news_list[0].keys()
with open('news.csv', 'w', newline='', encoding="UTF-8") as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames = keys)
    for line in eco_news_list:
        dict_writer.writerow(line)

# Проверка содержимого
for item in eco_news_list:
    i += 1
    print(f'{i}\nНазвание статьи: {item['name']}\nИсточник: {item['sourse']}\nСсылка: {item['link']}\nКонтент: {item['content']}\n')
