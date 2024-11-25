# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HomeworkItem(scrapy.Item):
    name = scrapy.Field()
    cost = scrapy.Field()
    url = scrapy.Field()
    rate = scrapy.Field()
    description = scrapy.Field()