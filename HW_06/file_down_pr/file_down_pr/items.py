# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Compose

# корректируем название фотографии
def process_name(value):
    value = '_'.join(value[0].split())
    return value

# выбираем последнюю ссылку из многих (у нее самое большое разрешение)
def process_photo(value):
    # value = [value.rindex('https://'):]
    value = (value[0].split(',')[-1]).split()[0]
    return value

# обработчики
class FileDownPrItem(scrapy.Item):
    name = scrapy.Field(input_processor=Compose(
        process_name), output_processor=TakeFirst())
    url = scrapy.Field()
    category = scrapy.Field()
    photos = scrapy.Field(input_processor=Compose(
        process_photo), output_processor=TakeFirst())
