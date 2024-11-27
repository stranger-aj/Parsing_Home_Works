# Создайте новый проект Scrapy. Дайте ему подходящее имя и убедитесь, что ваше окружение правильно настроено для работы с проектом.
# Создайте нового паука, способного перемещаться по сайту www.unsplash.com. Ваш паук должен уметь перемещаться по категориям фотографий 
# и получать доступ к страницам отдельных фотографий.
# Определите элемент (Item) в Scrapy, который будет представлять изображение. Ваш элемент должен включать такие детали, 
# как URL изображения, название изображения и категорию, к которой оно принадлежит.
# Используйте Scrapy ImagesPipeline для загрузки изображений. Обязательно установите параметр IMAGES_STORE в файле settings.py. 
# Убедитесь, что ваш паук правильно выдает элементы изображений, которые может обработать ImagesPipeline.
# Сохраните дополнительные сведения об изображениях (название, категория) в CSV-файле. Каждая строка должна соответствовать 
# одному изображению и содержать URL изображения, локальный путь к файлу (после загрузки), название и категорию.

import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from items import FileDownPrItem


class ImgSpiderSpider(scrapy.Spider):
    name = "img_spider"
    allowed_domains = ["unsplash.com"]
    # start_urls = ["https://unsplash.com"]

    # получение адреса стартовой станицы
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://unsplash.com/s/photos/{kwargs.get('query')}"]
        self.category = kwargs.get('query')

    # получение ссылок на изображения
    def parse(self, response: HtmlResponse):
        links = response.xpath("//div[@class='JM3zT']/a/@href")
        # print(*links, sep='\n')
        for link in links:
            yield response.follow(link, callback=self.parse_img)

    # получение полей элемента
    def parse_img(self, response: HtmlResponse):
        loader = ItemLoader(item=FileDownPrItem(), response=response)
        loader.add_xpath('name', "//div[@class='Tbd2Y']//img/@alt")
        loader.add_value('url', response.url)
        loader.add_value('category', self.category)
        loader.add_xpath('photos', "//div[@class='Tbd2Y']//img/@srcset")
        
        yield loader.load_item()
