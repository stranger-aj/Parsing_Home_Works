# Найдите сайт, содержащий интересующий вас список или каталог. Это может быть список книг, фильмов,
# спортивных команд или что-то еще, что вас заинтересовало.
# Создайте новый проект Scrapy и определите нового паука. С помощью атрибута start_urls укажите URL выбранной вами веб-страницы.
# Определите метод парсинга для извлечения интересующих вас данных. Используйте селекторы XPath или CSS для навигации по HTML
# и извлечения данных. Возможно, потребуется извлечь данные с нескольких страниц или перейти по ссылкам на другие страницы.
# Сохраните извлеченные данные в структурированном формате. Вы можете использовать оператор yield для возврата данных из паука,
# которые Scrapy может записать в файл в выбранном вами формате (например, JSON или CSV).
# Конечным результатом работы должен быть код Scrapy Spider, а также пример выходных данных.
# Не забывайте соблюдать правила robots.txt и условия обслуживания веб-сайта, а также ответственно подходите к использованию веб-скрейпинга.

import scrapy
from scrapy.http import HtmlResponse
from items import HomeworkItem


class BookWormSpider(scrapy.Spider):
    name = "book_worm"
    # книжный магазин лабиринт
    allowed_domains = ["www.labirint.ru"]
    # раздел эзотерики
    start_urls = ["https://www.labirint.ru/genres/2397/"]

    # ф-я парсинга ссылок на книги
    def parse(self, response: HtmlResponse):
        # print(HtmlResponse)
        links = response.xpath(
            "//div[contains(@class, 'product need-watch')]//a[@class='cover genres-cover']/@href").getall()
        # print(links)

        # вызываем ф-ю сбора данных для каждой книги на странице
        for link in links:
            try:
                yield response.follow("https://" + self.allowed_domains[0] + link, callback=self.book_info_parse)
            except:
                continue

        next_page = response.xpath(
            "//a[@class='pagination-next__text']/@href").get()
        if next_page:
            next_page = self.start_urls[0] + next_page
            # рекурсивно выбираем страницы
            yield response.follow(next_page, callback=self.parse)

    # функция сбора данных
    def book_info_parse(self, response: HtmlResponse):
        try:
            name = response.xpath("//div[@id='product-title']/h1/text()").get()
        except:
            name = None
        try:
            cost = float(response.xpath(
                "//span[@class='buying-pricenew-val-number']/text()").get())
        except:
            cost = None
        url = response.url
        try:
            rate = float(response.xpath("//div[@id='rate']/text()").get())
        except:
            rate = None
        try:
            desc_resp = (response.xpath(
                "//div[@id='product-about']/descendant::*/text()").getall())
            description = ' '.join(' '.join(desc_resp[1:]).split())
        except:
            desc_resp = None
        yield HomeworkItem(name=name, cost=cost, url=url, rate=rate, description=description)

# извлеченные Scrapy данные сохраняются в файле scrapy_result.json
# в файле settings.py: FEEDS = {'scrapy_result.json': {'format': 'json'}}
